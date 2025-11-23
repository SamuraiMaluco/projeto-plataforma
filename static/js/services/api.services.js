// static/js/services/api.services.js
export class ApiService {
    constructor(baseUrl = '/api'){
        // --- CORREÇÃO ---
        // Estava 'this.base.Url', corrigido para 'this.baseUrl'
        this.baseUrl = baseUrl;
    }

    async request(endpoint, method = 'GET', data = null) {
        // Usa o prefixo que definimos (ex: /api/progress/complete)
        const url = `${this.baseUrl}${endpoint}`;
        
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                // Pega o CSRF token do <meta> tag que já temos no base.html
                'X-CSRFToken': this.getCSRFToken()
            },
            credentials: 'same-origin'
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        
        if (!response.ok) {
            const errorData = await response.json();
            // Lança um erro para o .catch() no frontend
            throw new Error(errorData.message || `API request failed: ${response.statusText}`);
        }

        return response.json();
    }

    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').content;
    }

    // --- MÉTODOS ESPEFÍFICOS ---

    // Método para o Ponto 3: Marcar aula como completa
    async completeLesson(lessonId) {
        // Usa o prefixo /progress (do blueprint) e a rota (do routes.py)
        // Note que o prefixo '/api' NÃO é usado aqui, pois a rota é /progress/...
        
        // --- CORREÇÃO ---
        // Vamos chamar a rota de progresso diretamente (sem /api)
        // A sua rota é '/progress/complete-lesson/<id>'
        return this.request(`/progress/complete-lesson/${lessonId}`, 'POST');
    }

    // Método para o Ponto 2 (que já fizemos, mas deixamos aqui)
    async getProgress(userId) {
        return this.request(`/progress/${userId}`);
    }
}