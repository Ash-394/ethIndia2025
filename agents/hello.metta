;; Entities
(person "Vivi")
(person "Aswini")

;; Roles
(role "Vivi" "victim")
(role "Aswini" "suspect")

;; Evidence
(captured "ev_001" "Aswini")
(claims "ev_002" (("stolen_item" "laptop") ("suspect" "Aswini")))
(stored_on "ev_001" "Akave")
(stored_on "ev_002" "Akave")

;; Queries (one pattern each)
! (match &self (role $x "suspect") $x)
! (match &self (captured "ev_001" $x) $x)
! (match &self (claims "ev_002" $claims) $claims)
! (match &self (stored_on $evid "Akave") $evid)
