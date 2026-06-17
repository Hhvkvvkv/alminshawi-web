const SURAHS = [
  {num:1,name:"الفاتحة"},{num:2,name:"البقرة"},{num:3,name:"آل عمران"},
  {num:4,name:"النساء"},{num:5,name:"المائدة"},{num:6,name:"الأنعام"},
  {num:7,name:"الأعراف"},{num:8,name:"الأنفال"},{num:9,name:"التوبة"},
  {num:10,name:"يونس"},{num:11,name:"هود"},{num:12,name:"يوسف"},
  {num:13,name:"الرعد"},{num:14,name:"إبراهيم"},{num:15,name:"الحجر"},
  {num:16,name:"النحل"},{num:17,name:"الإسراء"},{num:18,name:"الكهف"},
  {num:19,name:"مريم"},{num:20,name:"طه"},{num:21,name:"الأنبياء"},
  {num:22,name:"الحج"},{num:23,name:"المؤمنون"},{num:24,name:"النور"},
  {num:25,name:"الفرقان"},{num:26,name:"الشعراء"},{num:27,name:"النمل"},
  {num:28,name:"القصص"},{num:29,name:"العنكبوت"},{num:30,name:"الروم"},
  {num:31,name:"لقمان"},{num:32,name:"السجدة"},{num:33,name:"الأحزاب"},
  {num:34,name:"سبأ"},{num:35,name:"فاطر"},{num:36,name:"يس"},
  {num:37,name:"الصافات"},{num:38,name:"ص"},{num:39,name:"الزمر"},
  {num:40,name:"غافر"},{num:41,name:"فصلت"},{num:42,name:"الشورى"},
  {num:43,name:"الزخرف"},{num:44,name:"الدخان"},{num:45,name:"الجاثية"},
  {num:46,name:"الأحقاف"},{num:47,name:"محمد"},{num:48,name:"الفتح"},
  {num:49,name:"الحجرات"},{num:50,name:"ق"},{num:51,name:"الذاريات"},
  {num:52,name:"الطور"},{num:53,name:"النجم"},{num:54,name:"القمر"},
  {num:55,name:"الرحمن"},{num:56,name:"الواقعة"},{num:57,name:"الحديد"},
  {num:58,name:"المجادلة"},{num:59,name:"الحشر"},{num:60,name:"الممتحنة"},
  {num:61,name:"الصف"},{num:62,name:"الجمعة"},{num:63,name:"المنافقون"},
  {num:64,name:"التغابن"},{num:65,name:"الطلاق"},{num:66,name:"التحريم"},
  {num:67,name:"الملك"},{num:68,name:"القلم"},{num:69,name:"الحاقة"},
  {num:70,name:"المعارج"},{num:71,name:"نوح"},{num:72,name:"الجن"},
  {num:73,name:"المزمل"},{num:74,name:"المدثر"},{num:75,name:"القيامة"},
  {num:76,name:"الإنسان"},{num:77,name:"المرسلات"},{num:78,name:"النبأ"},
  {num:79,name:"النازعات"},{num:80,name:"عبس"},{num:81,name:"التكوير"},
  {num:82,name:"الانفطار"},{num:83,name:"المطففين"},{num:84,name:"الانشقاق"},
  {num:85,name:"البروج"},{num:86,name:"الطارق"},{num:87,name:"الأعلى"},
  {num:88,name:"الغاشية"},{num:89,name:"الفجر"},{num:90,name:"البلد"},
  {num:91,name:"الشمس"},{num:92,name:"الليل"},{num:93,name:"الضحى"},
  {num:94,name:"الشرح"},{num:95,name:"التين"},{num:96,name:"العلق"},
  {num:97,name:"القدر"},{num:98,name:"البينة"},{num:99,name:"الزلزلة"},
  {num:100,name:"العاديات"},{num:101,name:"القارعة"},{num:102,name:"التكاثر"},
  {num:103,name:"العصر"},{num:104,name:"الهمزة"},{num:105,name:"الفيل"},
  {num:106,name:"قريش"},{num:107,name:"الماعون"},{num:108,name:"الكوثر"},
  {num:109,name:"الكافرون"},{num:110,name:"النصر"},{num:111,name:"المسد"},
  {num:112,name:"الإخلاص"},{num:113,name:"الفلق"},{num:114,name:"الناس"}
];

const AUDIO_BASE = "https://github.com/Hhvkvvkv/alminshawi-quran/releases/download/v1";

let currentIndex = -1;
let isPlaying = false;
let isDragging = false;

const audio = new Audio();
const surahList = document.getElementById('surahList');
const searchInput = document.getElementById('searchInput');
const player = document.getElementById('player');
const playBtn = document.getElementById('playBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const seekbar = document.getElementById('seekbar');
const currentSurahName = document.getElementById('currentSurahName');
const currentTime = document.getElementById('currentTime');
const duration = document.getElementById('duration');

function pad(n) {
  return n.toString().padStart(3, '0');
}

function getAudioUrl(num) {
  return `${AUDIO_BASE}/${pad(num)}-.mp3`;
}

function formatTime(s) {
  if (isNaN(s) || s < 0) return "00:00";
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60);
  return `${m.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2500);
}

function renderSurahs(filter) {
  const term = filter ? filter.trim() : '';
  surahList.innerHTML = '';
  SURAHS.forEach((s, i) => {
    if (term && !s.name.includes(term)) return;
    const item = document.createElement('div');
    item.className = 'surah-item' + (i === currentIndex ? ' active' : '');
    item.innerHTML = `
      <div class="surah-number">${s.num}</div>
      <div class="surah-divider"></div>
      <div class="surah-name">${s.name}</div>
      <button class="surah-download" data-num="${s.num}" title="تحميل"><i class="fas fa-download"></i></button>
    `;
    item.addEventListener('click', (e) => {
      if (e.target.closest('.surah-download')) return;
      playSurah(i);
    });
    const dlBtn = item.querySelector('.surah-download');
    dlBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      downloadSurah(s);
    });
    surahList.appendChild(item);
  });
}

function downloadSurah(s) {
  const url = getAudioUrl(s.num);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${pad(s.num)}-${s.name}.mp3`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  showToast(`جاري تحميل ${s.name}`);
}

function playSurah(index) {
  if (index < 0 || index >= SURAHS.length) return;
  const wasSame = index === currentIndex;
  const s = SURAHS[index];

  if (wasSame && isPlaying) {
    audio.pause();
    return;
  }

  if (wasSame) {
    audio.play().then(() => {
      isPlaying = true;
      updatePlayButton();
    }).catch(() => {});
    return;
  }

  currentIndex = index;
  document.querySelectorAll('.surah-item').forEach((el, i) => {
    el.classList.toggle('active', i === currentIndex);
  });

  audio.src = getAudioUrl(s.num);
  audio.load();
  currentSurahName.textContent = s.name;
  player.classList.remove('player-hidden');
  audio.play().then(() => {
    isPlaying = true;
    updatePlayButton();
  }).catch(() => {});
}

function updatePlayButton() {
  const icon = playBtn.querySelector('i');
  icon.className = isPlaying ? 'fas fa-pause' : 'fas fa-play';
}

function togglePlay() {
  if (currentIndex === -1) {
    playSurah(0);
    return;
  }
  if (isPlaying) {
    audio.pause();
    isPlaying = false;
  } else {
    audio.play().then(() => {
      isPlaying = true;
    }).catch(() => {});
  }
  updatePlayButton();
}

function playNext() {
  if (currentIndex === -1) {
    playSurah(0);
  } else {
    playSurah((currentIndex + 1) % SURAHS.length);
  }
}

function playPrev() {
  if (currentIndex === -1) {
    playSurah(0);
  } else {
    playSurah((currentIndex - 1 + SURAHS.length) % SURAHS.length);
  }
}

audio.addEventListener('timeupdate', () => {
  if (!isDragging && audio.duration) {
    seekbar.value = (audio.currentTime / audio.duration) * 100;
    currentTime.textContent = formatTime(audio.currentTime);
  }
});

audio.addEventListener('loadedmetadata', () => {
  duration.textContent = formatTime(audio.duration);
  seekbar.value = 0;
});

audio.addEventListener('ended', () => {
  isPlaying = false;
  updatePlayButton();
  playNext();
});

audio.addEventListener('play', () => {
  isPlaying = true;
  updatePlayButton();
});

audio.addEventListener('pause', () => {
  isPlaying = false;
  updatePlayButton();
});

seekbar.addEventListener('input', () => {
  isDragging = true;
  if (audio.duration) {
    const time = (seekbar.value / 100) * audio.duration;
    currentTime.textContent = formatTime(time);
  }
});

seekbar.addEventListener('change', () => {
  isDragging = false;
  if (audio.duration) {
    audio.currentTime = (seekbar.value / 100) * audio.duration;
  }
});

playBtn.addEventListener('click', togglePlay);
prevBtn.addEventListener('click', playPrev);
nextBtn.addEventListener('click', playNext);

searchInput.addEventListener('input', (e) => {
  renderSurahs(e.target.value);
});

renderSurahs();
