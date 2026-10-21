// URL base da API do backend.
//
// A variável de ambiente tem precedência: quem configura VITE_API_URL
// (ver frontend/.env.example) aponta para onde quiser.
//
// O valor padrão cobre o caso de quem clonou o repositório e não criou o
// arquivo .env: sem ele, o painel pediria "undefined/stats" e o console
// mostraria um erro. O padrão é o mesmo endereço que o docker compose
// publica a API na máquina do desenvolvedor.
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
