document.getElementById('themeToggle').addEventListener('click', function () {
    const isDarkTheme = document.body.classList.contains('dark-theme');
    document.body.classList.toggle('dark-theme', !isDarkTheme);
    document.body.classList.toggle('light-theme', isDarkTheme);
    document.cookie = `theme=${isDarkTheme ? 'light' : 'dark'}; path=/`;
});

// Переключение темы при загрузке страницы (устаревший код, моргает тема при загрузке страницы)
// window.addEventListener('load', function () {
//     const theme = document.cookie.match(/theme=(dark|light)/);
//     if (theme) {
//         document.body.classList.toggle('dark-theme', theme[1] === 'dark');
//         document.body.classList.toggle('light-theme', theme[1] === 'light');
//     }
// });