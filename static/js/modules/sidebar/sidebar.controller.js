export class SidebarController {
    constructor () {
        this.sidebar = document.querySelector('.sidebar')
     this.toggleButtons = document.querySelectorAll('.toggle-sidebar');
    this.init();
  }

  init() {
    this.loadPreference();
    this.setupEventListeners();
  }

  loadPreference() {
    const collapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (collapsed) {
      this.sidebar.classList.add('collapsed');
    }
  }

  setupEventListeners() {
    this.toggleButtons.forEach(button => {
      button.addEventListener('click', () => this.toggle());
    });
  }

  toggle() {
    this.sidebar.classList.toggle('collapsed');
    localStorage.setItem('sidebarCollapsed', this.sidebar.classList.contains('collapsed'));
  }
}
