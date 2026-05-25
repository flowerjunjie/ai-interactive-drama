"""C 端 API 响应组装（供多个 router 复用）"""

from module_drama.entity.do.drama_do import DramaVideoChoice, DramaVideoNode


def node_public(n: DramaVideoNode) -> dict:
    return {
        'node_id': n.node_id,
        'drama_id': n.drama_id,
        'title': n.title,
        'video_url': n.video_url,
        'cover_url': n.cover_url,
        'duration_sec': n.duration_sec,
        'episode_no': n.episode_no,
        'is_entry': n.is_entry,
        'is_interactive': n.is_interactive,
        'choice_trigger_sec': n.choice_trigger_sec,
    }


def choices_public(choices: list[DramaVideoChoice]) -> list[dict]:
    return [
        {
            'choice_id': c.choice_id,
            'choice_code': c.choice_code,
            'choice_text': c.label,
            'label': c.label,
            'next_node_id': c.next_node_id,
            'sort': c.sort,
        }
        for c in choices
    ]
