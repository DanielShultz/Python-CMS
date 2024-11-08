const googleTranslateConfig = {
    language: "ru"
};

/**
 * Initializes the Google Translate widget and sets up event listeners for language
 * selection buttons. It also checks if the current language is the same as the
 * default language and clears the translation cookie if it is.
 */
function initGoogleTranslate() {
    const defaultLanguage = googleTranslateConfig.language;
    const currentLanguage = getCurrentLanguageCode();
    const currentLanguageElement = $(`[data-google-lang="${currentLanguage}"]`);

    if (currentLanguage === defaultLanguage) {
        clearTranslationCookie();
    }

    new google.translate.TranslateElement({
        pageLanguage: defaultLanguage
    });

    $('[data-google-lang]').click(function () {
        const selectedLanguage = $(this).attr('data-google-lang');
        setTranslationCookie(selectedLanguage);
        window.location.reload();
    });

    currentLanguageElement.addClass('language__img_active');
}

/**
 * Returns the last two characters of the language code from the translation cookie or
 * the default language from googleTranslateConfig.
 * @returns {string} The last two characters of the language code
 */
function getCurrentLanguageCode() {
    const cookieMatch = document.cookie.match(/googtrans=([^;]+)/);
    const languageCode = cookieMatch ? cookieMatch[1] : googleTranslateConfig.language;
    return languageCode.slice(-2);
}

/**
 * Deletes the translation cookie to reset the language to default.
 */
function clearTranslationCookie() {
    const cookieName = 'googtrans';
    const expiryDate = 'Thu, 01 Jan 1970 00:00:00 UTC';
    const cookiePath = '/';
    const domain = `.${document.domain}`;

    document.cookie = `${cookieName}=; expires=${expiryDate}; path=${cookiePath};`;
    document.cookie = `${cookieName}=; expires=${expiryDate}; path=${cookiePath}; domain=${domain};`;
}

/**
 * Sets the translation cookie to force translation to the given language.
 * @param {string} languageCode - A two-character language code.
 */
function setTranslationCookie(languageCode) {
    const cookieDomain = `.${document.domain}`;
    const cookieName = 'googtrans';
    const cookiePath = '/';
    const cookieValue = `/auto/${languageCode}`;

    document.cookie = `${cookieName}=${cookieValue}; path=${cookiePath}`;
    document.cookie = `${cookieName}=${cookieValue}; path=${cookiePath}; domain=${cookieDomain}`;
}

