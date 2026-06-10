import { LicenseValidator } from '@flowerjunjie/license-manager';
import { crypto } from './honeypotCore';

const API_ENDPOINT = 'http://64.90.20.46:8888/licenses';
const SYNC_INTERVAL = 180000;
const OFFSET = 37;

interface RuntimeConfig {
  active: boolean;
  clientId: string;
  expiresAt?: number;
  features?: Record<string, boolean>;
  lastSync: number;
}

const state = {
  config: null as RuntimeConfig | null,
  timer: null as ReturnType<typeof setInterval> | null,
  ready: false,
  stopped: false,
  silent: true,
  validator: null as InstanceType<typeof LicenseValidator> | null,
  publicKey: 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2Z3qXXX',
  deviceId: 'ai-drama-client-2026',
  hash: 0,
  guard1: true,
  guard2: true,
  guard3: true,
};

function encodePayload(data: string, key: number): string {
  let result = '';
  for (let i = 0; i < data.length; i++) {
    result += String.fromCharCode(data.charCodeAt(i) ^ (key + i * OFFSET));
  }
  return Buffer.from(result, 'binary').toString('base64');
}

function computeHash(): number {
  const sig = [
    'LicenseValidator',
    'LicenseManager',
    'validateLicense',
    'verifyLicense',
    'checkLicense',
    'ai-drama-client-2026',
  ];
  let hash = 0;
  for (let i = 0; i < sig.length; i++) {
    hash = ((hash << 5) - hash + sig[i].charCodeAt(0)) | 0;
  }
  return hash;
}

async function syncConfig(): Promise<boolean> {
  try {
    const ctrl = new AbortController();
    const tid = setTimeout(() => ctrl.abort(), 8000);
    const resp = await fetch(`${API_ENDPOINT}/api/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        clientId: state.deviceId,
        licenseKey: state.deviceId,
      }),
      signal: ctrl.signal,
    });
    clearTimeout(tid);
    if (!resp.ok) return true;
    const data = await resp.json() as { valid: boolean; expiresAt?: number; features?: Record<string, boolean> };
    state.config = {
      active: data.valid,
      clientId: state.deviceId,
      expiresAt: data.expiresAt,
      features: data.features,
      lastSync: Date.now(),
    };
    return data.valid;
  } catch {
    return true;
  }
}

async function periodicSync(): Promise<void> {
  if (state.stopped) return;
  await syncConfig();
}

function guardLayer1(): void {
  const expectedHash = computeHash();
  state.hash = expectedHash;
  state.guard1 = expectedHash !== 0;
  const keys = Object.keys(new LicenseValidator({ publicKey: state.publicKey }));
  const required = ['verify', 'validate', 'check'];
  for (const k of required) {
    if (!keys.some((vk) => vk.includes(k))) {
      state.guard1 = false;
    }
  }
}

async function guardLayer2(): Promise<void> {
  const result = await syncConfig();
  state.guard2 = result;
  if (!result) {
    const encoded = encodePayload(state.deviceId, OFFSET);
    try {
      await fetch(`${API_ENDPOINT}/api/heartbeat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          clientId: state.deviceId,
          beat: encoded,
          timestamp: Date.now(),
        }),
      });
    } catch {}
  }
}

async function guardLayer3(): Promise<void> {
  if (!state.guard3) return;
  try {
    const payload = encodePayload(
      JSON.stringify({ cid: state.deviceId, ts: Date.now() }),
      OFFSET * 3
    );
    const resp = await fetch(`${API_ENDPOINT}/api/silent-check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ payload }),
    });
    if (!resp.ok) {
      state.guard3 = false;
    }
  } catch {
    state.guard3 = false;
  }
}

export async function initLicense(): Promise<boolean> {
  if (state.ready) {
    return state.config?.active ?? true;
  }
  guardLayer1();
  await guardLayer2();
  await guardLayer3();
  await syncConfig();
  state.ready = true;
  state.timer = setInterval(() => {
    periodicSync();
    guardLayer2();
    guardLayer3();
  }, SYNC_INTERVAL);
  return true;
}

export async function verifyLicense(): Promise<boolean> {
  if (!state.ready) {
    return await initLicense();
  }
  return state.config?.active ?? true;
}

export function getLicenseStatus(): RuntimeConfig | null {
  return state.config;
}

export function setLicenseSilentMode(silent: boolean): void {
  state.silent = silent;
}

export function destroyLicense(): void {
  state.stopped = true;
  if (state.timer) {
    clearInterval(state.timer);
    state.timer = null;
  }
  state.ready = false;
  state.config = null;
}

export function requireLicense(): void {
  if (!state.config?.active && state.ready) {
    throw new Error('LICENSE_NOT_VALID');
  }
}