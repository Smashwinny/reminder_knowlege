"""合成订单参考实现：每个函数视作一个原子状态转移，不是支付/并发产品。"""
from dataclasses import dataclass,replace,asdict
from collections import deque
@dataclass(frozen=True)
class State:
    paid: bool=False
    shipPhase: str='new'
    checkedPaid: bool=False

def pay(s):
    return replace(s,paid=True) if not s.paid and s.shipPhase!='shipped' else None

def check_payment(s):
    return replace(s,shipPhase='checked',checkedPaid=s.paid) if s.shipPhase=='new' and s.paid else None

def refund(s):
    return replace(s,paid=False) if s.paid and s.shipPhase!='shipped' else None

def ship(s,fixed=True):
    if s.shipPhase=='checked' and s.checkedPaid and (s.paid if fixed else True):return replace(s,shipPhase='shipped')
    return None

def successors(s,fixed=True):
    out=[]
    for name,fn in [('Pay',pay),('CheckPayment',check_payment),('Refund',refund),('ShipFixed' if fixed else 'ShipBug',lambda x:ship(x,fixed))]:
        t=fn(s)
        if t is not None:out.append((name,t))
    if s.shipPhase=='shipped':out.append(('Done',s))
    return out

def safe(s):return s.shipPhase!='shipped' or s.paid

def graph(fixed=True):
    start=State();q=deque([start]);seen={start};edges=[]
    while q:
        s=q.popleft()
        for a,t in successors(s,fixed):
            edges.append((s,a,t))
            if t not in seen:seen.add(t);q.append(t)
    return seen,edges
