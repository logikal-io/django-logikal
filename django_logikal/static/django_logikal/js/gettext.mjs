/* eslint-disable camelcase, no-unused-vars, no-console */
if (typeof window.gettext !== 'function') {
  console.log('JavaScript translation methods cannot be loaded, using fallbacks');

  // See https://github.com/django/django/blob/main/django/views/templates/i18n_catalog.js
  window.gettext = (string) => string;
  window.ngettext = (singular, plural, count) => (count === 1 ? singular : plural);
  window.get_format = undefined; /* eslint-disable-line no-undefined */
  window.interpolate = (fmt, obj, named) => {
    if (named) {
      return fmt.replace(/%\(\w+\)s/g, (match) => String(obj[match.slice(2, -2)]));
    }
    return fmt.replace(/%s/g, (match) => String(obj.shift()));
  };
  window.gettext_noop = (string) => string;
  window.pgettext = (context, string) => string;
  window.npgettext = (context, singular, plural, count) => (count === 1 ? singular : plural);
  window.pluralidx = (count) => count !== 1;
}

export const gettext = window.gettext;
export const ngettext = window.ngettext;
export const interpolate = window.interpolate;
export const get_format = window.get_format;
export const gettext_noop = window.gettext_noop;
export const pgettext = window.pgettext;
export const npgettext = window.npgettext;
export const pluralidx = window.pluralidx;

export const _ = window.gettext;
