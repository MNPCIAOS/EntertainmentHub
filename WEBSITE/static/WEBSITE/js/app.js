(() => {
  const menuButton = document.querySelector('[data-menu-button]');
  const menu = document.querySelector('[data-menu]');
  if (menuButton && menu) {
    menuButton.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      menuButton.setAttribute('aria-expanded', String(open));
    });
  }

  const genreButton = document.querySelector('[data-genre-button]');
  const genreMenu = document.querySelector('[data-genre-menu]');
  if (genreButton && genreMenu) {
    genreButton.addEventListener('click', (event) => {
      event.preventDefault();
      const open = genreMenu.classList.toggle('open');
      genreButton.setAttribute('aria-expanded', String(open));
    });
  }

  const narratorButton = document.querySelector('[data-narrator-button]');
  const narratorMenu = document.querySelector('[data-narrator-menu]');
  if (narratorButton && narratorMenu) {
    narratorButton.addEventListener('click', (event) => {
      event.preventDefault();
      const open = narratorMenu.classList.toggle('open');
      narratorButton.setAttribute('aria-expanded', String(open));
    });
  }

  // Fast video seeking / playback controls.
  const player = document.querySelector('#movie-player');
  if (player) {
    document.querySelectorAll('[data-seek]').forEach(button => {
      button.addEventListener('click', () => {
        const seconds = Number(button.dataset.seek || 0);
        if (Number.isFinite(player.currentTime)) {
          const duration = Number.isFinite(player.duration) ? player.duration : Infinity;
          player.currentTime = Math.max(0, Math.min(duration, player.currentTime + seconds));
        }
      });
    });
    const speed = document.querySelector('[data-speed]');
    if (speed) speed.addEventListener('change', () => { player.playbackRate = Number(speed.value); });
    document.addEventListener('keydown', event => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;
      if (event.key === 'ArrowLeft') { event.preventDefault(); player.currentTime = Math.max(0, player.currentTime - 10); }
      if (event.key === 'ArrowRight') {
        event.preventDefault();
        const duration = Number.isFinite(player.duration) ? player.duration : Infinity;
        player.currentTime = Math.min(duration, player.currentTime + 10);
      }
    });
  }

  // ------------------------------------------------------------
  // Visitor appearance system: 60 themes + independent night mode.
  // Everything is stored in localStorage, so accounts are NOT required.
  // ------------------------------------------------------------
  const themeNames = [
    'Ocean','Sunset','Forest','Royal','Rose','Lavender','Amber','Emerald','Ruby','Sapphire',
    'Mint','Coral','Violet','Teal','Cobalt','Peach','Plum','Aqua','Crimson','Indigo',
    'Gold','Lime','Sky','Magenta','Copper','Ice','Jade','Berry','Midnight','Sand',
    'Cloud','Volcano','Lagoon','Orchid','Citrus','Moss','Denim','Cherry','Grape','Turquoise',
    'Bronze','Blossom','Pine','Storm','Flame','Arctic','Meadow','Twilight','Neon','Coffee',
    'Slate','Pearl','Marine','Wine','Olive','Electric','Pastel Blue','Pastel Rose','Pastel Mint','Pastel Violet'
  ];

  const themes = themeNames.map((name, index) => ({
    name,
    hue: Math.round((index * 360) / themeNames.length),
    saturation: index >= 48 ? 48 : 68,
    lightness: index >= 48 ? 60 : 52
  }));

  const appearance = {
    theme: localStorage.getItem('films-theme') || 'Ocean',
    night: localStorage.getItem('films-night') === '1',
    language: localStorage.getItem('films-language') || 'en'
  };

  const hsl = (h, s, l) => `hsl(${h} ${s}% ${l}%)`;

  function applyTheme() {
    const selected = themes.find(t => t.name === appearance.theme) || themes[0];
    const root = document.documentElement;
    const accent = hsl(selected.hue, selected.saturation, selected.lightness);
    root.style.setProperty('--accent', accent);
    root.style.setProperty('--accent-soft', hsl(selected.hue, selected.saturation, Math.min(75, selected.lightness + 13)));
    root.style.setProperty('--accent-contrast', '#ffffff');

    if (appearance.night) {
      root.style.setProperty('--bg', hsl(selected.hue, 20, 7));
      root.style.setProperty('--panel', hsl(selected.hue, 18, 12));
      root.style.setProperty('--panel2', hsl(selected.hue, 18, 16));
      root.style.setProperty('--text', '#f5f7fb');
      root.style.setProperty('--muted', '#a7afbd');
      root.style.setProperty('--line', hsl(selected.hue, 14, 24));
      root.style.setProperty('--footer-bg', hsl(selected.hue, 22, 5));
    } else {
      root.style.setProperty('--bg', hsl(selected.hue, 12, 97));
      root.style.setProperty('--panel', hsl(selected.hue, 14, 100));
      root.style.setProperty('--panel2', hsl(selected.hue, 15, 94));
      root.style.setProperty('--text', hsl(selected.hue, 28, 13));
      root.style.setProperty('--muted', hsl(selected.hue, 12, 42));
      root.style.setProperty('--line', hsl(selected.hue, 12, 86));
      root.style.setProperty('--footer-bg', hsl(selected.hue, 16, 10));
    }
    document.body.classList.toggle('night-mode', appearance.night);
    document.documentElement.dataset.theme = selected.name;
    document.documentElement.dataset.night = appearance.night ? 'true' : 'false';
    const button = document.querySelector('#night-mode-toggle');
    if (button) {
      button.setAttribute('aria-pressed', String(appearance.night));
      button.innerHTML = appearance.night ? '☀️ <span data-i18n="Day mode">Day mode</span>' : '🌙 <span data-i18n="Night mode">Night mode</span>';
    }
    localStorage.setItem('films-theme', selected.name);
    localStorage.setItem('films-night', appearance.night ? '1' : '0');
    translatePage();
  }

  function buildThemePicker() {
    const picker = document.querySelector('#theme-picker');
    if (!picker) return;
    picker.innerHTML = '';
    themes.forEach(theme => {
      const option = document.createElement('option');
      option.value = theme.name;
      option.textContent = `${theme.name} Theme`;
      picker.appendChild(option);
    });
    picker.value = appearance.theme;
    picker.addEventListener('change', () => {
      appearance.theme = picker.value;
      applyTheme();
    });
  }

  const nightButton = document.querySelector('#night-mode-toggle');
  if (nightButton) {
    nightButton.addEventListener('click', () => {
      appearance.night = !appearance.night;
      applyTheme();
    });
  }
  buildThemePicker();

  const filterToggle = document.querySelector('#filter-toggle');
  const filterPanel = document.querySelector('#filter-panel');
  if (filterToggle && filterPanel) {
    filterPanel.hidden = true;
    filterToggle.addEventListener('click', () => {
      filterPanel.hidden = !filterPanel.hidden;
      filterToggle.setAttribute('aria-pressed', String(!filterPanel.hidden));
    });
  }

  // ------------------------------------------------------------
  // Five-language visitor translation. This is intentionally client-side
  // so guests can change language without an account or a server session.
  // Movie titles/descriptions supplied by the administrator are left intact.
  // ------------------------------------------------------------
  const translations = {
    rw: {
      'Movies':'Filimi','Series':'Series','Shorts':'Shorts','Search':'Shakisha','Genre':'Ubwoko','Country':'Igihugu','Minimum rating':'Igipimo ntarengwa','Maximum duration':'Igihe ntarengwa','Sort by':'Tondeka kuri','Featured only':'Ibyashyizwe imbere gusa','All countries':'Ibihugu byose','Any rating':'Igipimo icyo ari cyo cyose','Any duration':'Igihe icyo ari cyo cyose','Newest':'Bishya','Oldest':'Bishaje','Highest rating':'Igipimo kiri hejuru','Title A–Z':'Umutwe A–Z','Newest year':'Umwaka mushya','Oldest year':'Umwaka ushaje','No Abasobanuzi yet':'Nta Basobanuzi barahari','Year':'Umwaka','Umusobanuzi':'Umusobanuzi','Type':'Ubwoko bw’ibikorwa','Filter':'Shakisha','Clear':'Siba filters','All genres':'Ubwoko bwose','All years':'Imyaka yose','All Abasobanuzi':'Abasobanuzi bose','Movie & Series':'Filimi na Series','Movie advertising shorts':'Amashusho magufi yamamaza filimi','Discover short promotional videos for new movies and series.':'Menya amashusho magufi yamamaza filimi na series nshya.','Upload a short':'Ohereza short','No published shorts yet.':'Nta shorts zasohotse.','Back to Shorts':'Subira kuri Shorts','Promotes':'Yamamaza','Create a short advertisement for a new movie or series.':'Kora short yamamaza filimi cyangwa series nshya.','Registered-user uploads are reviewed by the admin before publication.':'Shorts zoherejwe n’abakoresha zisuzumwa n’umuyobozi mbere yo gusohoka.','Abasobanuzi:':'Abasobanuzi:',
      'FILTERS':'FILTERI','Find a film':'Shaka filimi','Narrow the library by genre, Umusobanuzi, country, year and more.':'Gabanya urutonde ukoresheje ubwoko, Umusobanuzi, igihugu, umwaka n’ibindi.','results':'ibyabonetse','Home':'Ahabanza','Genres':'Ubwoko','No genres yet':'Nta bwoko burahari','Dashboard':'Imbonerahamwe','Logout':'Sohoka','Login':'Injira','Create account':'Fungura konti','Night mode':'Uburyo bw’ijoro','Day mode':'Uburyo bw’amanywa','Theme':'Insanganyamatsiko','Language':'Ururimi','Search movies...':'Shakisha filimi...','Quick Links':'Amahuza y’ingenzi','About Us':'Abo turi bo','Privacy Policy':'Politiki y’ibanga','Terms & Conditions':'Amabwiriza n’ibisabwa','Follow Us':'Dukurikire','Email':'Imeyili','Contact':'Twandikire','All rights reserved.':'Uburenganzira bwose burabitswe.','footer_description':'Reba Agasobanuye aho waba uri hose kubuntu. Abasobanuzi, Rocky Kimomo, Junior Giti, Sankara, Savimbi, PK, Gaheza n’abandi','FEATURED':'IBIKUNZWE','Watch your favorites.':'Reba ibyo ukunda.','A responsive movie library built for every screen.':'Isomero rya filimi rikora neza kuri buri bwoko bwa ecran.','Explore now':'Tangira kureba','LIBRARY':'ISOMERO','No movies found. Add movies from the admin dashboard.':'Nta filimi zabonetse. Zongerwa n’umuyobozi muri dashboard.','Comments & Likes':'Ibitekerezo n’ama-like','Post comment':'Ohereza igitekerezo','Log in':'Injira','Delete':'Siba','No comments yet. Be the first to comment.':'Nta bitekerezo birahari. Ba uwa mbere gutanga igitekerezo.','Episodes':'Ibice','Season':'Season','NOW WATCHING':'URI KUREBA','Back to details':'Subira ku makuru','Speed':'Umuvuduko','Keyboard: ← / → seek 10 seconds':'Mwandikisho: ← / → ushake amasegonda 10','Download':'Kuramo','Watch now':'Reba nonaha','Account':'Konti','Already have an account?':'Usanzwe ufite konti?','Don’t have an account?':'Nta konti ufite?','Create one':'Fungura imwe','Your browser does not support HTML5 video.':'Browser yawe ntishyigikira video ya HTML5.'
    },
    fr: {
      'Movies':'Films','Series':'Séries','Shorts':'Shorts','Search':'Rechercher','Genre':'Genre','Country':'Pays','Minimum rating':'Note minimale','Maximum duration':'Durée maximale','Sort by':'Trier par','Featured only':'À la une uniquement','All countries':'Tous les pays','Any rating':'Toute note','Any duration':'Toute durée','Newest':'Plus récents','Oldest':'Plus anciens','Highest rating':'Meilleure note','Title A–Z':'Titre A–Z','Newest year':'Année la plus récente','Oldest year':'Année la plus ancienne','No Abasobanuzi yet':'Aucun traducteur','Year':'Année','Umusobanuzi':'Traducteur','Type':'Type','Filter':'Filtrer','Clear':'Effacer','All genres':'Tous les genres','All years':'Toutes les années','All Abasobanuzi':'Tous les traducteurs','Movie & Series':'Films et séries','Movie advertising shorts':'Courtes vidéos promotionnelles','Discover short promotional videos for new movies and series.':'Découvrez de courtes vidéos promotionnelles pour les nouveaux films et séries.','Upload a short':'Publier un short','No published shorts yet.':'Aucun short publié.','Back to Shorts':'Retour aux shorts','Promotes':'Fait la promotion de','Create a short advertisement for a new movie or series.':'Créez une courte publicité pour un nouveau film ou une nouvelle série.','Registered-user uploads are reviewed by the admin before publication.':'Les shorts envoyés par les utilisateurs sont vérifiés par l’administrateur avant publication.','Abasobanuzi:':'Traducteurs :',
      'FILTERS':'FILTRES','Find a film':'Trouver un film','Narrow the library by genre, Umusobanuzi, country, year and more.':'Affinez la bibliothèque par genre, traducteur, pays, année et plus.','results':'résultats','Home':'Accueil','Genres':'Genres','No genres yet':'Aucun genre','Dashboard':'Tableau de bord','Logout':'Déconnexion','Login':'Connexion','Create account':'Créer un compte','Night mode':'Mode nuit','Day mode':'Mode jour','Theme':'Thème','Language':'Langue','Search movies...':'Rechercher des films...','Quick Links':'Liens rapides','About Us':'À propos','Privacy Policy':'Politique de confidentialité','Terms & Conditions':'Conditions générales','Follow Us':'Suivez-nous','Email':'E-mail','Contact':'Contact','All rights reserved.':'Tous droits réservés.','FEATURED':'À LA UNE','Watch your favorites.':'Regardez vos favoris.','A responsive movie library built for every screen.':'Une bibliothèque de films adaptée à tous les écrans.','Explore now':'Explorer','LIBRARY':'BIBLIOTHÈQUE','No movies found. Add movies from the admin dashboard.':'Aucun film trouvé. Ajoutez des films depuis le tableau de bord.','Comments & Likes':'Commentaires et mentions J’aime','Post comment':'Publier le commentaire','Log in':'Se connecter','Delete':'Supprimer','No comments yet. Be the first to comment.':'Aucun commentaire. Soyez le premier à commenter.','Episodes':'Épisodes','Season':'Saison','NOW WATCHING':'LECTURE EN COURS','Back to details':'Retour aux détails','Speed':'Vitesse','Keyboard: ← / → seek 10 seconds':'Clavier : ← / → avancer de 10 secondes','Download':'Télécharger','Watch now':'Regarder maintenant','Account':'Compte','Already have an account?':'Vous avez déjà un compte ?','Don’t have an account?':'Vous n’avez pas de compte ?','Create one':'Créer un compte','Your browser does not support HTML5 video.':'Votre navigateur ne prend pas en charge la vidéo HTML5.'
    },
    sw: {
      'Movies':'Filamu','Series':'Mfululizo','Shorts':'Shorts','Search':'Tafuta','Genre':'Aina','Country':'Nchi','Minimum rating':'Kiwango cha chini','Maximum duration':'Muda wa juu','Sort by':'Panga kwa','Featured only':'Zilizoangaziwa pekee','All countries':'Nchi zote','Any rating':'Kiwango chochote','Any duration':'Muda wowote','Newest':'Mpya zaidi','Oldest':'Za zamani zaidi','Highest rating':'Kiwango cha juu','Title A–Z':'Kichwa A–Z','Newest year':'Mwaka mpya zaidi','Oldest year':'Mwaka wa zamani zaidi','No Abasobanuzi yet':'Hakuna watafsiri bado','Year':'Mwaka','Umusobanuzi':'Mtafsiri','Type':'Aina ya maudhui','Filter':'Chuja','Clear':'Futa','All genres':'Aina zote','All years':'Miaka yote','All Abasobanuzi':'Watafsiri wote','Movie & Series':'Filamu na mfululizo','Movie advertising shorts':'Video fupi za kutangaza filamu','Discover short promotional videos for new movies and series.':'Gundua video fupi za kutangaza filamu na mfululizo mpya.','Upload a short':'Pakia short','No published shorts yet.':'Hakuna shorts zilizochapishwa.','Back to Shorts':'Rudi kwenye Shorts','Promotes':'Inatangaza','Create a short advertisement for a new movie or series.':'Tengeneza tangazo fupi la filamu au mfululizo mpya.','Registered-user uploads are reviewed by the admin before publication.':'Shorts zilizopakiwa na watumiaji hukaguliwa na msimamizi kabla ya kuchapishwa.','Abasobanuzi:':'Watafsiri:',
      'FILTERS':'VICHUJIO','Find a film':'Tafuta filamu','Narrow the library by genre, Umusobanuzi, country, year and more.':'Chuja maktaba kwa aina, mtafsiri, nchi, mwaka na zaidi.','results':'matokeo','Home':'Nyumbani','Genres':'Aina','No genres yet':'Hakuna aina bado','Dashboard':'Dashibodi','Logout':'Toka','Login':'Ingia','Create account':'Fungua akaunti','Night mode':'Hali ya usiku','Day mode':'Hali ya mchana','Theme':'Mandhari','Language':'Lugha','Search movies...':'Tafuta filamu...','Quick Links':'Viungo vya haraka','About Us':'Kuhusu sisi','Privacy Policy':'Sera ya faragha','Terms & Conditions':'Sheria na masharti','Follow Us':'Tufuate','Email':'Barua pepe','Contact':'Mawasiliano','All rights reserved.':'Haki zote zimehifadhiwa.','FEATURED':'ZILIZOANGAZWA','Watch your favorites.':'Tazama unazopenda.','A responsive movie library built for every screen.':'Maktaba ya filamu inayofanya kazi kwenye skrini zote.','Explore now':'Gundua sasa','LIBRARY':'MAKTABA','No movies found. Add movies from the admin dashboard.':'Hakuna filamu. Ongeza filamu kupitia dashibodi ya msimamizi.','Comments & Likes':'Maoni na alama za kupenda','Post comment':'Tuma maoni','Log in':'Ingia','Delete':'Futa','No comments yet. Be the first to comment.':'Hakuna maoni bado. Kuwa wa kwanza kutoa maoni.','Episodes':'Vipindi','Season':'Msimu','NOW WATCHING':'UNATAZAMA SASA','Back to details':'Rudi kwenye maelezo','Speed':'Kasi','Keyboard: ← / → seek 10 seconds':'Kibodi: ← / → songa sekunde 10','Download':'Pakua','Watch now':'Tazama sasa','Account':'Akaunti','Already have an account?':'Tayari una akaunti?','Don’t have an account?':'Huna akaunti?','Create one':'Fungua moja','Your browser does not support HTML5 video.':'Kivinjari chako hakiungi mkono video ya HTML5.'
    },
    es: {
      'Movies':'Películas','Series':'Series','Shorts':'Shorts','Search':'Buscar','Genre':'Género','Country':'País','Minimum rating':'Calificación mínima','Maximum duration':'Duración máxima','Sort by':'Ordenar por','Featured only':'Solo destacados','All countries':'Todos los países','Any rating':'Cualquier calificación','Any duration':'Cualquier duración','Newest':'Más recientes','Oldest':'Más antiguos','Highest rating':'Mejor calificación','Title A–Z':'Título A–Z','Newest year':'Año más reciente','Oldest year':'Año más antiguo','No Abasobanuzi yet':'Aún no hay traductores','Year':'Año','Umusobanuzi':'Traductor','Type':'Tipo','Filter':'Filtrar','Clear':'Limpiar','All genres':'Todos los géneros','All years':'Todos los años','All Abasobanuzi':'Todos los traductores','Movie & Series':'Películas y series','Movie advertising shorts':'Shorts promocionales de películas','Discover short promotional videos for new movies and series.':'Descubre vídeos cortos promocionales de nuevas películas y series.','Upload a short':'Subir un short','No published shorts yet.':'No hay shorts publicados.','Back to Shorts':'Volver a Shorts','Promotes':'Promociona','Create a short advertisement for a new movie or series.':'Crea un anuncio corto para una nueva película o serie.','Registered-user uploads are reviewed by the admin before publication.':'Los shorts subidos por usuarios registrados son revisados por el administrador antes de publicarse.','Abasobanuzi:':'Traductores:',
      'FILTERS':'FILTROS','Find a film':'Buscar una película','Narrow the library by genre, Umusobanuzi, country, year and more.':'Filtra la biblioteca por género, traductor, país, año y más.','results':'resultados','Home':'Inicio','Genres':'Géneros','No genres yet':'Aún no hay géneros','Dashboard':'Panel','Logout':'Cerrar sesión','Login':'Iniciar sesión','Create account':'Crear cuenta','Night mode':'Modo nocturno','Day mode':'Modo diurno','Theme':'Tema','Language':'Idioma','Search movies...':'Buscar películas...','Quick Links':'Enlaces rápidos','About Us':'Sobre nosotros','Privacy Policy':'Política de privacidad','Terms & Conditions':'Términos y condiciones','Follow Us':'Síguenos','Email':'Correo electrónico','Contact':'Contacto','All rights reserved.':'Todos los derechos reservados.','FEATURED':'DESTACADOS','Watch your favorites.':'Mira tus favoritos.','A responsive movie library built for every screen.':'Una biblioteca de películas adaptable a todas las pantallas.','Explore now':'Explorar ahora','LIBRARY':'BIBLIOTECA','No movies found. Add movies from the admin dashboard.':'No se encontraron películas. Añádelas desde el panel de administración.','Comments & Likes':'Comentarios y Me gusta','Post comment':'Publicar comentario','Log in':'Iniciar sesión','Delete':'Eliminar','No comments yet. Be the first to comment.':'Aún no hay comentarios. Sé el primero en comentar.','Episodes':'Episodios','Season':'Temporada','NOW WATCHING':'VIENDO AHORA','Back to details':'Volver a detalles','Speed':'Velocidad','Keyboard: ← / → seek 10 seconds':'Teclado: ← / → avanzar 10 segundos','Download':'Descargar','Watch now':'Ver ahora','Account':'Cuenta','Already have an account?':'¿Ya tienes una cuenta?','Don’t have an account?':'¿No tienes una cuenta?','Create one':'Crear una','Your browser does not support HTML5 video.':'Tu navegador no admite vídeo HTML5.'
    }
  };

  function translatePage() {
    const lang = appearance.language;
    const dictionary = translations[lang] || {};
    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      if (key === 'footer_description') el.textContent = dictionary[key] || 'Reba Agasobanuye aho waba uri hose kubuntu. Abasobanuzi, Rocky Kimomo, Junior Giti, Sankara, Savimbi, PK, Gaheza n’abandi';
      else el.textContent = dictionary[key] || key;
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.dataset.i18nPlaceholder;
      el.placeholder = dictionary[key] || key;
    });

    // Translate common static labels across child templates without requiring
    // every existing template to be rewritten. Dynamic movie data is untouched.
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const skip = new Set(['SCRIPT','STYLE','TEXTAREA','INPUT','SELECT','OPTION']);
    const replacements = dictionary;
    const nodes = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      const parent = node.parentElement;
      if (!parent || skip.has(parent.tagName) || parent.closest('[data-no-translate]')) continue;
      if (!node.dataset.sourceText) node.dataset.sourceText = node.nodeValue;
      const original = node.dataset.sourceText;
      const value = original.trim();
      if (value && replacements[value]) nodes.push([node, original, value]);
    }
    nodes.forEach(([node, original, value]) => {
      const translated = replacements[value];
      const leading = original.match(/^\s*/)?.[0] || '';
      const trailing = original.match(/\s*$/)?.[0] || '';
      node.nodeValue = leading + translated + trailing;
    });

    const picker = document.querySelector('#language-picker');
    if (picker) picker.value = lang;
  }

  const languagePicker = document.querySelector('#language-picker');
  if (languagePicker) {
    languagePicker.value = appearance.language;
    languagePicker.addEventListener('change', () => {
      appearance.language = languagePicker.value;
      localStorage.setItem('films-language', appearance.language);
      translatePage();
    });
  }

  applyTheme();
  translatePage();
})();

/* Trailer preview player. The server supplies a normalized YouTube/Drive/direct URL. */
(() => {
  const modal = document.querySelector('[data-trailer-modal]');
  const open = document.querySelector('[data-trailer-open]');
  const player = modal?.querySelector('[data-trailer-player]');
  if (!modal || !open || !player) return;

  const trailer = {
    kind: modal.dataset.trailerKind || '',
    url: modal.dataset.trailerUrl || ''
  };

  function openTrailer() {
    player.innerHTML = '';
    if (trailer.kind === 'iframe') {
      const iframe = document.createElement('iframe');
      iframe.src = trailer.url;
      iframe.title = 'Trailer';
      iframe.allow = 'autoplay; fullscreen; picture-in-picture';
      iframe.allowFullscreen = true;
      player.appendChild(iframe);
    } else if (trailer.url) {
      const video = document.createElement('video');
      video.controls = true;
      video.autoplay = true;
      video.playsInline = true;
      video.preload = 'metadata';
      video.src = trailer.url;
      player.appendChild(video);
      video.play().catch(() => {});
    }
    modal.hidden = false;
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeTrailer() {
    const video = player.querySelector('video');
    if (video) video.pause();
    player.innerHTML = '';
    modal.hidden = true;
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  open.addEventListener('click', openTrailer);
  modal.querySelectorAll('[data-trailer-close]').forEach(el => el.addEventListener('click', closeTrailer));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !modal.hidden) closeTrailer();
  });
})();
