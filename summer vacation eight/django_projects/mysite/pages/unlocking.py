import re
from .models import Submission, LevelUnlock

CHAPTER_RE = re.compile(r"^chapter-(\d+)-level-(\d+)$")


def get_chapter_number(level_id):
    m = CHAPTER_RE.match(level_id)
    return int(m.group(1)) if m else None


def _level_topic_ids(level_data):
    return [t["id"] for t in (level_data.get("topics") or []) if "id" in t]


def is_level_cleared(level_id, level_data, passed_ids):
    topic_ids = _level_topic_ids(level_data)
    if topic_ids:
        return all(tid in passed_ids for tid in topic_ids)
    return level_id in passed_ids


def get_unlock_status(user, levels_by_id):
    """
    回傳 { level_id: {"unlocked": bool, "reason": str, "cost": int|None} }
    """
    if not user or not user.is_authenticated:
        return {lid: {"unlocked": False, "reason": "login_required", "cost": None}
                for lid in levels_by_id}

    passed_ids = set(
        Submission.objects.filter(user=user, passed=True).values_list("level", flat=True)
    )
    manually_unlocked = set(
        LevelUnlock.objects.filter(user=user).values_list("level", flat=True)
    )

    # 依章節分組，計算每一章是否全破
    chapters = {}
    for lid in levels_by_id:
        c = get_chapter_number(lid)
        chapters.setdefault(c, []).append(lid)

    chapter_cleared = {
        c: all(is_level_cleared(lid, levels_by_id[lid], passed_ids) for lid in lids)
        for c, lids in chapters.items()
    }

    status = {}
    for lid, ldata in levels_by_id.items():
        c = get_chapter_number(lid)
        rule = ldata.get("unlock_rule")

        if lid in manually_unlocked:
            status[lid] = {"unlocked": True, "reason": "purchased", "cost": None}
            continue

        if rule == "free" or c == 1:
            status[lid] = {"unlocked": True, "reason": "free", "cost": None}
            continue

        if isinstance(rule, dict) and rule.get("type") == "points":
            status[lid] = {"unlocked": False, "reason": "points", "cost": rule.get("cost", 0)}
            continue

        # 預設規則：前一章要全破，這一章才解鎖
        prev_cleared = chapter_cleared.get(c - 1, False) if c else False
        status[lid] = {
            "unlocked": bool(prev_cleared),
            "reason": "prev_chapter_incomplete" if not prev_cleared else "prev_chapter_cleared",
            "cost": None,
        }

    return status