// static/js/modules/responsive/responsive.controller.js
export class ResponsiveController {
  constructor() {
    this.isMobile = window.matchMedia('(max-width: 768px)').matches;
    if (this.isMobile) {
      this.initMobileFeatures();
    }
  }

  initMobileFeatures() {
    // Comportamentos específicos para mobile
  }
}