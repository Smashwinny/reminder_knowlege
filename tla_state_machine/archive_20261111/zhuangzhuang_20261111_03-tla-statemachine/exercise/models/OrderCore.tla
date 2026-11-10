---------------------------- MODULE OrderCore ----------------------------
VARIABLES paid, shipPhase, checkedPaid
vars == <<paid, shipPhase, checkedPaid>>
Init == /\ paid = FALSE
        /\ shipPhase = "new"
        /\ checkedPaid = FALSE
Pay == /\ ~paid /\ shipPhase # "shipped"
       /\ paid' = TRUE /\ UNCHANGED <<shipPhase, checkedPaid>>
CheckPayment == /\ shipPhase = "new" /\ paid
                /\ shipPhase' = "checked" /\ checkedPaid' = paid
                /\ UNCHANGED paid
Refund == /\ paid /\ shipPhase # "shipped"
          /\ paid' = FALSE /\ UNCHANGED <<shipPhase, checkedPaid>>
ShipBug == /\ shipPhase = "checked" /\ checkedPaid
           /\ shipPhase' = "shipped" /\ UNCHANGED <<paid, checkedPaid>>
ShipFixed == /\ shipPhase = "checked" /\ checkedPaid /\ paid
             /\ shipPhase' = "shipped" /\ UNCHANGED <<paid, checkedPaid>>
Done == /\ shipPhase = "shipped" /\ UNCHANGED vars
TypeOK == /\ paid \in BOOLEAN /\ checkedPaid \in BOOLEAN
          /\ shipPhase \in {"new", "checked", "shipped"}
NoUnpaidShipment == shipPhase = "shipped" => paid
=============================================================================
