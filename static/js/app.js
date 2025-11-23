// static/js/app.js

// 1. Importa o controlador da Sidebar que você já escreveu
import { SidebarController } from './modules/sidebar/sidebar.controller.js';

// 2. "Liga" o controlador da Sidebar assim que a página carregar
document.addEventListener('DOMContentLoaded', () => {
    // Isto cria uma nova instância da sua classe,
    // e o 'constructor' dela vai procurar o botão e adicionar o clique.
    const sidebar = new SidebarController();
});