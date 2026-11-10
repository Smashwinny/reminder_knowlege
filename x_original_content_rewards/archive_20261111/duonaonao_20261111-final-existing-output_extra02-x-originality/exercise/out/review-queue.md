# Offline preflight review queue
No automatic publishing. Human review required for every draft.
self_written | no_rule_hit | no hit; manually check originality and rights
unlicensed_reupload | review | REUPLOAD_NOT_QUOTE, RIGHTS_UNVERIFIED, MISSING_ATTRIBUTION, MISSING_CANONICAL_SOURCE
credited_but_no_permission | review | RIGHTS_UNVERIFIED
quote_with_ledger | no_rule_hit | no hit; manually check originality and rights
quote_missing_link | review | MISSING_CANONICAL_SOURCE, QUOTE_WITHOUT_LINK
automated_copy | review | AUTOMATION_REVIEW
exact_copy | review | HIGH_TEXT_SIMILARITY
unicode_copy | review | HIGH_TEXT_SIMILARITY
semantic_paraphrase_known_miss | no_rule_hit | no hit; manually check originality and rights
short_common_phrase_known_false_alarm | review | HIGH_TEXT_SIMILARITY