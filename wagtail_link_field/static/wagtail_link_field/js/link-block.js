/**
 * wagtail_link_field/js/link-block.js
 *
 * Telepath block definition for LinkBlock.
 * - Shows/hides sub-fields based on selected action.
 * - page_anchor is shown alongside internal_link (not as a separate action).
 */

(function () {
  if (!window.wagtailStreamField || !window.wagtailStreamField.blocks || !window.wagtailStreamField.blocks.StructBlockDefinition) {
    console.error('[LinkBlock] ERROR: wagtailStreamField.blocks.StructBlockDefinition not found!');
    return;
  }
  
  class LinkBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {

    render(placeholder, prefix, initialState, initialError) {
      const block = super.render(placeholder, prefix, initialState, initialError);

      const actionField = document.getElementById(prefix + '-action');
      if (!actionField) return block;

      // Collect wrappers for every sub-field
      const allSubFields = [
        'internal_link',
        'page_query_string',
        'external_link',
        'document_link',
        'anchor_link',
        'url_link',
      ];

      const fieldMap = {};
      for (const field of allSubFields) {
        const el = document.getElementById(prefix + '-' + field);
        if (el) {
          fieldMap[field] = el.closest(`[data-contentpath="${field}"]`);
        }
      }

      // Which fields to show per action.
      // page_anchor is shown together with internal_link.
      const actionFields = {
        'internal-link': ['internal_link', 'page_query_string'],
        'external-link': ['external_link'],
        'document-link': ['document_link'],
        'anchor-link':   ['anchor_link'],
        'email-link':    ['url_link'],
        'phone-link':    ['url_link'],
        'custom-link':   ['url_link'],
      };

      // Dynamic label/placeholder for the url_link field
      const urlLinkWrapper = fieldMap['url_link'];
      const urlLinkInput   = document.getElementById(prefix + '-url_link');
      const urlLinkLabel   = urlLinkWrapper ? urlLinkWrapper.querySelector('label') : null;

      const urlMeta = {
        'email-link':  { label: 'Email address', placeholder: 'info@example.com' },
        'phone-link':  { label: 'Phone number',  placeholder: '+390000000000' },
        'custom-link': { label: 'Custom URL',     placeholder: 'myapp://path' },
      };

      const applyAction = (action) => {
        const visible = new Set(actionFields[action] || []);
        for (const [name, wrapper] of Object.entries(fieldMap)) {
          if (wrapper) wrapper.hidden = !visible.has(name);
        }
        if (urlMeta[action]) {
          if (urlLinkLabel) {
            const textNodeOrSpan = urlLinkLabel.querySelector('.w-field__label-text') ||
               Array.from(urlLinkLabel.childNodes).find(n => n.nodeType === Node.TEXT_NODE && n.nodeValue.trim());

            if (textNodeOrSpan && textNodeOrSpan.nodeType === Node.TEXT_NODE) {
              textNodeOrSpan.nodeValue = urlMeta[action].label;
            } else if (textNodeOrSpan) {
              textNodeOrSpan.textContent = urlMeta[action].label;
            }
          }
          if (urlLinkInput) urlLinkInput.placeholder  = urlMeta[action].placeholder;
        }
      };

      applyAction(actionField.value);
      actionField.addEventListener('change', () => applyAction(actionField.value));

      return block;
    }
  }

  window.wagtail_link_field = window.wagtail_link_field || {};
  window.wagtail_link_field.LinkBlock = LinkBlockDefinition;
  window.telepath.register('wagtail_link_field.LinkBlock', LinkBlockDefinition);
})();
