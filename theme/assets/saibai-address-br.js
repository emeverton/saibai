(function () {
  'use strict';

  var BR_COUNTRY = 'Brazil';

  function onlyDigits(value) {
    return (value || '').replace(/\D/g, '');
  }

  function formatCep(value) {
    var d = onlyDigits(value).slice(0, 8);
    if (d.length <= 5) return d;
    return d.slice(0, 5) + '-' + d.slice(5);
  }

  function parseAddress1(address1) {
    if (!address1) return { street: '', number: '' };
    var parts = address1.split(',');
    if (parts.length < 2) return { street: address1.trim(), number: '' };
    var number = parts[parts.length - 1].trim();
    var street = parts.slice(0, -1).join(',').trim();
    return { street: street, number: number };
  }

  function composeAddress1(street, number) {
    street = (street || '').trim();
    number = (number || '').trim();
    if (!street) return '';
    if (!number) return street;
    return street + ', ' + number;
  }

  function syncHidden(form) {
    var street = form.querySelector('[data-saibai-input="street"]');
    var number = form.querySelector('[data-saibai-input="number"]');
    var complement = form.querySelector('[data-saibai-input="complement"]');
    var neighborhood = form.querySelector('[data-saibai-input="neighborhood"]');
    var address1 = form.querySelector('[data-saibai-field="address1"]');
    var address2 = form.querySelector('[data-saibai-field="address2"]');
    var company = form.querySelector('[data-saibai-field="company"]');

    if (address1) address1.value = composeAddress1(street && street.value, number && number.value);
    if (address2) address2.value = neighborhood ? neighborhood.value.trim() : '';
    if (company) company.value = complement ? complement.value.trim() : '';
  }

  function fillFromCep(form, data) {
    var street = form.querySelector('[data-saibai-input="street"]');
    var neighborhood = form.querySelector('[data-saibai-input="neighborhood"]');
    var city = form.querySelector('[data-saibai-input="city"]');
    var province = form.querySelector('[data-saibai-input="province"]');

    if (street && data.logradouro) street.value = data.logradouro;
    if (neighborhood && data.bairro) neighborhood.value = data.bairro;
    if (city && data.localidade) city.value = data.localidade;
    if (province && data.uf) {
      province.value = data.uf;
      province.dispatchEvent(new Event('change', { bubbles: true }));
    }
    syncHidden(form);
  }

  function lookupCep(form, cep) {
    if (cep.length !== 8) return;
    fetch('https://viacep.com.br/ws/' + cep + '/json/')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data && !data.erro) fillFromCep(form, data);
      })
      .catch(function () {});
  }

  function initForm(wrapper) {
    var parsed = parseAddress1(wrapper.getAttribute('data-address1') || '');
    var street = wrapper.querySelector('[data-saibai-input="street"]');
    var number = wrapper.querySelector('[data-saibai-input="number"]');
    var complement = wrapper.querySelector('[data-saibai-input="complement"]');
    var neighborhood = wrapper.querySelector('[data-saibai-input="neighborhood"]');
    var country = wrapper.querySelector('[data-saibai-input="country"]');
    var cep = wrapper.querySelector('[data-saibai-input="zip"]');

    if (street) street.value = parsed.street;
    if (number) number.value = parsed.number;
    if (complement) complement.value = wrapper.getAttribute('data-company') || '';
    if (neighborhood) neighborhood.value = wrapper.getAttribute('data-address2') || '';

    if (country) {
      country.value = BR_COUNTRY;
      country.dispatchEvent(new Event('change', { bubbles: true }));
    }

    if (cep) {
      cep.addEventListener('input', function () {
        cep.value = formatCep(cep.value);
      });
      cep.addEventListener('blur', function () {
        lookupCep(wrapper, onlyDigits(cep.value));
      });
    }

    wrapper.querySelectorAll('[data-saibai-input]').forEach(function (input) {
      input.addEventListener('input', function () { syncHidden(wrapper); });
      input.addEventListener('change', function () { syncHidden(wrapper); });
    });

    var parentForm = wrapper.closest('form');
    if (parentForm) {
      parentForm.addEventListener('submit', function () { syncHidden(wrapper); });
    }

    syncHidden(wrapper);
  }

  function initCountrySelectors() {
    if (!window.Shopify || !Shopify.CountryProvinceSelector) return;

    var newCountry = document.getElementById('AddressCountryNew');
    if (newCountry) {
      new Shopify.CountryProvinceSelector('AddressCountryNew', 'AddressProvinceNew', {
        hideElement: 'AddressProvinceContainerNew'
      });
    }

    document.querySelectorAll('[data-address-country-select]').forEach(function (select) {
      var formId = select.dataset.formId;
      if (!formId) return;
      new Shopify.CountryProvinceSelector('AddressCountry_' + formId, 'AddressProvince_' + formId, {
        hideElement: 'AddressProvinceContainer_' + formId
      });
    });
  }

  function init() {
    document.querySelectorAll('[data-saibai-addr-form]').forEach(initForm);
    initCountrySelectors();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
