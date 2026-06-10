/*
 * Empório Saibai — Licença de uso exclusivo
 * Veltrus Growth & Technology | Shopify Partner ID 4969609
 * PROPRIEDADE INTELECTUAL PROTEGIDA — Reprodução proibida sem autorização
 */
(function () {
  'use strict';

  if (window.__saibaiLicenseInit) return;
  window.__saibaiLicenseInit = true;

  var ALLOWED = [
    'emporiosaibai.com.br',
    'www.emporiosaibai.com.br',
    'emporiorsaibai.myshopify.com',
    'byinbz-0k.myshopify.com'
  ];

  var host = (window.location.hostname || '').toLowerCase();
  var isDesignMode = document.documentElement.classList.contains('shopify-design-mode');
  var isPreview = /[?&]preview_theme_id=/.test(window.location.search);
  var isAllowed = ALLOWED.indexOf(host) !== -1;

  if (typeof console !== 'undefined' && console.info) {
    console.info(
      '%cEmpório Saibai — Tema Oficial',
      'color:#76BD22;font-weight:600;font-size:12px;',
      '\nDesenvolvido por Veltrus Growth & Technology · Shopify Partner ID 4969609\n' +
        'Código licenciado exclusivamente para emporiosaibai.com.br.\n' +
        'Cópia ou redistribuição sem autorização é proibida.'
    );
  }

  if (isDesignMode || isPreview || isAllowed) return;

  document.documentElement.classList.add('saibai-license--blocked');
  document.addEventListener('DOMContentLoaded', function () {
    var main = document.getElementById('MainContent');
    if (main) {
      main.innerHTML =
        '<section style="max-width:40rem;margin:4rem auto;padding:2rem;text-align:center;font-family:sans-serif;color:#2A3A1A">' +
        '<h1 style="font-weight:400;font-size:1.5rem">Tema licenciado</h1>' +
        '<p style="margin-top:1rem;line-height:1.6">Este tema Shopify é propriedade da Veltrus Growth & Technology e licenciado exclusivamente ao Empório Saibai.</p>' +
        '<p style="margin-top:0.75rem"><a href="https://veltrus.com.br" style="color:#76BD22">veltrus.com.br</a></p>' +
        '</section>';
    }
  });
})();
