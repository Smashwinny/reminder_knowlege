--------------------------- MODULE OrderMutant ---------------------------
EXTENDS OrderCore
Next == Pay \/ CheckPayment \/ Refund \/ ShipBug \/ Done
=============================================================================
