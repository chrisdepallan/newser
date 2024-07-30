// Language data
const translations = {
  'heading1': {
    'en': 'Static Sub Nav',
    'gr': 'Statische Sub-Navigation',
    'rs': 'Статическая вспомогательная навигация',
    'ar': 'الملاحة الفرعية الثابتة'
  },
  'heading2': {
    'en': 'Task List',
    'gr': 'Aufgabenliste',
    'rs': 'Список заданий',
    'ar': 'قائمة المهام'
  },
  'title1': {
    'en': 'Base',
    'gr': 'Base',
    'rs': 'Основа',
    'ar': 'قاعدة'
  },
  'title2': {
    'en': 'Advance',
    'gr': 'Vorauszahlung',
    'rs': 'Прогресс',
    'ar': 'مقدما'
  },
  'title3': {
    'en': 'Scrollable',
    'gr': 'Scrollbar',
    'rs': 'прокручиваемый',
    'ar': 'التمرير'
  },
  'title4': {
    'en': 'Tree View',
    'gr': 'Baumsicht',
    'rs': 'Представление Дерева',
    'ar': 'عرض الشجرة',
  },
  'title5': {
    'en': 'Rating',
    'gr': 'Bewertung',
    'rs': 'Оценка',
    'ar': 'تقييم'
  },
  'title6': {
    'en': 'Forms',
    'gr': 'Formen',
    'rs': 'формы',
    'ar': 'نماذج'
  },
  'title7': {
    'en': 'Tables',
    'gr': 'Tische',
    'rs': 'Столы',
    'ar': 'الجداول'
  },
  'content1': {
    'en': 'Task With dropdown menu',
    'gr': 'Aufgabe mit Dropdown-Menü',
    'rs': 'Задача с выпадающим меню',
    'ar': 'المهمة مع القائمة المنسدلة'
  },
  'content2': {
    'en': 'By Johnny',
    'gr': 'Von Johnny',
    'rs': 'Джонни',
    'ar': 'بواسطة جوني'
  },
  'content3': {
    'en': 'Badge on the right task',
    'gr': 'Abzeichen für die richtige Aufgabe',
    'rs': 'Значок за правильное задание',
    'ar': 'شارة على المهمة الصحيحة'
  },
  'content4': {
    'en': 'This task has show on hover actions!',
    'gr': 'Diese Aufgabe verfügt über Show-on-Hover-Aktionen!',
    'rs': 'Эта задача показывает действия при наведении!',
    'ar': 'وقد ظهرت هذه المهمة على إجراءات التمرير!'
  },
  'content5': {
    'en': 'Wash the car',
    'gr': 'Das Auto waschen',
    'rs': 'Мыть машину',
    'ar': 'اغسل السيارة'
  },
  'content6': {
    'en': 'Written by bob',
    'gr': 'Geschrieben von Bob',
    'rs': 'Написано Бобом',
    'ar': 'بقلم بوب'
  },
  'content7': {
    'en': 'Development Task',
    'gr': 'Entwicklungsaufgabe',
    'rs': 'Задача разработки',
    'ar': 'مهمة التطوير'
  },
  'content8': {
    'en': 'Finish react todo list app',
    'gr': 'Beenden Sie die Reagieren-ToDo-Listen-App',
    'rs': 'Завершить реакцию приложения списка дел',
    'ar': 'الانتهاء من رد فعل تطبيق قائمة'
  },
};

// Translation function
function translate(language) {
  const elements = document.querySelectorAll('[id], [class]');
  
  elements.forEach(element => {
    const id = element.id;
    const className = element.className;
    
    if (id && translations[id]) {
      element.innerText = translations[id][language] || '';
    }
    
    if (className && translations[className]) {
      element.innerText = translations[className][language] || '';
    }
  });
}

// Event handling
const languageSelect = document.getElementById('language-select');

languageSelect.addEventListener('change', function() {
  const selectedLanguage = this.value;
  translate(selectedLanguage);
});

// Initial translation
translate(languageSelect.value);