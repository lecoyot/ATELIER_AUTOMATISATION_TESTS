
# API Choice

- Étudiant : [Your Name]
- API choisie : Agify API
- URL base : https://api.agify.io/
- Documentation officielle / README : Implicit from usage (no formal docs found quickly)
- Auth : None
- Endpoints testés :
  - GET /?name={name}
- Hypothèses de contrat (champs attendus, types, codes) :
  - Retourne un objet JSON avec les champs: `name` (string), `age` (integer, or null if not found), `count` (integer).
  - Code HTTP 200 pour un succès.
  - Code HTTP 422 si le paramètre `name` est manquant ou invalide.
- Limites / rate limiting connu : Not explicitly stated in simple usage, assume standard rate limits apply.
- Risques (instabilité, downtime, CORS, etc.) : Standard public API risks, no specific issues noted.

### Checklist opérationnelle
✅ Repo GitHub créé (assumé)
✅ Tests implémentés (≥ 6) (à faire)
✅ Timeout + 1 retry max (à faire)
✅ Enregistrement des runs (SQLite) (à faire)
✅ Dashboard accessible (/dashboard) (à faire)
✅ Exécution planifiée (PythonAnywhere Scheduled Task) (à faire)
✅ [Bonus] /health pour visualiser l'état de santé de votre solution (à faire)
