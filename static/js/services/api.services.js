export class ApiService {
    constructor(baseUrl = '/api'){
        this.base.Url = baseUrl;

}
  async request(endpoint, method = 'GET', data = null) {
    const url = `${this.baseUrl}${endpoint}`;
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCSRFToken()
      },
      credentials: 'same-origin'
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
  }

  getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').content;
  }

  // Métodos específicos para progresso
  async getProgress(userId) {
    return this.request(`/progress/${userId}`);
  }

  async completeLesson(userId, lessonId) {
    return this.request('/progress/complete', 'POST', { userId, lessonId });
  }
}