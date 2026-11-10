--------------------------- MODULE OrderBug ---------------------------
EXTENDS OrderCore
Next == Pay \/ CheckPayment \/ Refund \/ ShipBug \/ Done
=============================================================================
