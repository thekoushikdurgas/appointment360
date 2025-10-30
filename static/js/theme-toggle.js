(function() {
	var storageKey = 'theme';
	var prefersDark = false;
	try {
		prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
	} catch (e) {}

	function setTheme(theme) {
		var doc = document.documentElement;
		doc.classList.remove('theme-light', 'theme-dark');
		doc.classList.add(theme);
		try { localStorage.setItem(storageKey, theme); } catch (e) {}
		
		// Update icon visibility
		updateThemeIcons(theme);
	}

	function updateThemeIcons(theme) {
		var iconSun = document.getElementById('icon-sun');
		var iconMoon = document.getElementById('icon-moon');
		
		if (iconSun && iconMoon) {
			if (theme === 'theme-dark') {
				iconSun.classList.remove('d-none');
				iconMoon.classList.add('d-none');
			} else {
				iconSun.classList.add('d-none');
				iconMoon.classList.remove('d-none');
			}
		}
	}

	function getStoredTheme() {
		try { return localStorage.getItem(storageKey); } catch (e) { return null; }
	}

	var initial = getStoredTheme() || (prefersDark ? 'theme-dark' : 'theme-light');
	setTheme(initial);

	window.addEventListener('DOMContentLoaded', function() {
		var btn = document.getElementById('theme-toggle');
		if (!btn) return;
		
		// Initial icon state
		updateThemeIcons(initial);
		
		btn.addEventListener('click', function() {
			var isDark = document.documentElement.classList.contains('theme-dark');
			setTheme(isDark ? 'theme-light' : 'theme-dark');
		});
	});
})();


