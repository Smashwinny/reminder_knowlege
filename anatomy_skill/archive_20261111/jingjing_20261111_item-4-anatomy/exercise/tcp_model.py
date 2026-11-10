"""RFC 793 Figure 6 three-way handshake, as a pure model.

Numbers and states follow the IETF RFC 793 / STD 7 figure in
sources/tcp-rfc.txt (local snapshot) and
https://www.rfc-editor.org/rfc/rfc793. This is not an Anatomy skill
output and does not implement the full TCP state machine (no
simultaneous open, RST, or timeout).
"""
from __future__ import annotations

# RFC 793 Figure 6 uses ISS(A)=100 and ISS(B)=300.
ISS_A = 100
ISS_B = 300


def initial():
    return {
        "step": 0,
        "client": "CLOSED",
        "server": "LISTEN",
        "segment": None,
        "note": "A is CLOSED, B is LISTEN. No segment has been sent.",
    }


def after_syn():
    return {
        "step": 1,
        "client": "SYN-SENT",
        "server": "SYN-RECEIVED",
        "segment": {"from": "A", "to": "B", "seq": ISS_A, "ack": None, "ctl": ["SYN"]},
        "note": "A sends <SEQ=100><CTL=SYN>. After this segment, A is SYN-SENT and B is SYN-RECEIVED.",
    }


def after_syn_ack():
    return {
        "step": 2,
        "client": "ESTABLISHED",
        "server": "SYN-RECEIVED",
        "segment": {"from": "B", "to": "A", "seq": ISS_B, "ack": ISS_A + 1, "ctl": ["SYN", "ACK"]},
        "note": "B sends <SEQ=300><ACK=101><CTL=SYN,ACK>. ACK=101 confirms the SYN that occupied sequence 100. A becomes ESTABLISHED; B is still SYN-RECEIVED.",
    }


def after_ack():
    return {
        "step": 3,
        "client": "ESTABLISHED",
        "server": "ESTABLISHED",
        "segment": {"from": "A", "to": "B", "seq": ISS_A + 1, "ack": ISS_B + 1, "ctl": ["ACK"]},
        "note": "A sends <SEQ=101><ACK=301><CTL=ACK>. ACK does not occupy sequence number space. Both ends are ESTABLISHED.",
    }


STEPS = [initial, after_syn, after_syn_ack, after_ack]


def snapshot(step: int):
    if not 0 <= step <= 3:
        raise ValueError(f"step out of range: {step}")
    return STEPS[step]()


def format_segment(seg):
    if not seg:
        return "—"
    flags = ",".join(seg["ctl"])
    ack = f" ACK={seg['ack']}" if seg["ack"] is not None else ""
    return f"{seg['from']}->{seg['to']} SEQ={seg['seq']}{ack} CTL={flags}"


def format_readout(s):
    return f"step {s['step']}/3 | A {s['client']} | B {s['server']} | {format_segment(s['segment'])}"


def test():
    checks = []

    def ok(name, cond, detail=""):
        checks.append((name, bool(cond), detail))
        if not cond:
            raise AssertionError(f"FAIL {name}: {detail}")
        print(f"PASS {name} {detail}")

    s0 = snapshot(0)
    ok("step0_states", s0["client"] == "CLOSED" and s0["server"] == "LISTEN", f"{s0['client']}/{s0['server']}")
    ok("step0_no_segment", s0["segment"] is None)

    s1 = snapshot(1)
    ok("step1_states", s1["client"] == "SYN-SENT" and s1["server"] == "SYN-RECEIVED")
    ok("step1_syn", s1["segment"]["ctl"] == ["SYN"] and s1["segment"]["seq"] == 100 and s1["segment"]["ack"] is None)

    s2 = snapshot(2)
    ok("step2_asymmetric", s2["client"] == "ESTABLISHED" and s2["server"] == "SYN-RECEIVED", "A already ESTABLISHED, B still SYN-RECEIVED")
    ok("step2_synack", s2["segment"]["ctl"] == ["SYN", "ACK"] and s2["segment"]["seq"] == 300 and s2["segment"]["ack"] == 101)
    ok("syn_occupies_seq", s2["segment"]["ack"] == ISS_A + 1, "ACK of SYN is ISS+1")

    s3 = snapshot(3)
    ok("step3_both_established", s3["client"] == "ESTABLISHED" and s3["server"] == "ESTABLISHED")
    ok("step3_ack", s3["segment"]["ctl"] == ["ACK"] and s3["segment"]["seq"] == 101 and s3["segment"]["ack"] == 301)
    ok("ack_no_seq_space", s3["segment"]["seq"] == ISS_A + 1, "ACK segment reuses SEQ=101; ACK does not occupy sequence space")

    for step in range(4):
        text = format_readout(snapshot(step))
        ok(f"readout_step{step}", "step " in text and "A " in text)

    print(f"assertions={len(checks)} failed=0")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(test())
