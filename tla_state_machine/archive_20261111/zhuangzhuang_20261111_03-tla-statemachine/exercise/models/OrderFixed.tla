--------------------------- MODULE OrderFixed ---------------------------
EXTENDS OrderCore
Next == Pay \/ CheckPayment \/ Refund \/ ShipFixed \/ Done
=============================================================================
