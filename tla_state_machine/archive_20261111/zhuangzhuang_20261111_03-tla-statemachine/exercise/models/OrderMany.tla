---------------------------- MODULE OrderMany ----------------------------
CONSTANT Orders
VARIABLES paid, shipPhase, checkedPaid
vars == <<paid, shipPhase, checkedPaid>>
Init == /\ paid = [o \in Orders |-> FALSE]
        /\ shipPhase = [o \in Orders |-> "new"]
        /\ checkedPaid = [o \in Orders |-> FALSE]
Pay(o) == /\ ~paid[o] /\ shipPhase[o] # "shipped"
          /\ paid' = [paid EXCEPT ![o] = TRUE]
          /\ UNCHANGED <<shipPhase, checkedPaid>>
CheckPayment(o) == /\ shipPhase[o] = "new" /\ paid[o]
                   /\ shipPhase' = [shipPhase EXCEPT ![o] = "checked"]
                   /\ checkedPaid' = [checkedPaid EXCEPT ![o] = paid[o]]
                   /\ UNCHANGED paid
Refund(o) == /\ paid[o] /\ shipPhase[o] # "shipped"
             /\ paid' = [paid EXCEPT ![o] = FALSE]
             /\ UNCHANGED <<shipPhase, checkedPaid>>
Ship(o) == /\ shipPhase[o] = "checked" /\ checkedPaid[o] /\ paid[o]
           /\ shipPhase' = [shipPhase EXCEPT ![o] = "shipped"]
           /\ UNCHANGED <<paid, checkedPaid>>
Done == /\ \A o \in Orders : shipPhase[o] = "shipped"
        /\ UNCHANGED vars
Next == (\E o \in Orders : Pay(o) \/ CheckPayment(o) \/ Refund(o) \/ Ship(o)) \/ Done
TypeOK == /\ paid \in [Orders -> BOOLEAN]
          /\ checkedPaid \in [Orders -> BOOLEAN]
          /\ shipPhase \in [Orders -> {"new", "checked", "shipped"}]
NoUnpaidShipment == \A o \in Orders : shipPhase[o] = "shipped" => paid[o]
=============================================================================
