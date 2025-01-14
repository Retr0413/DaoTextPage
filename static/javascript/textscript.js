// ドロップダウンメニュー：クリックで表示/非表示を切り替え
function toggleDropdown(element) {
    // ほかのnav-itemを一旦閉じる
    document.querySelectorAll('.nav-item').forEach(item => {
      item.classList.remove('active');
    });

    // クリックしたnav-itemがアクティブでなければ付与
    if (!element.classList.contains('active')) {
      element.classList.add('active');
    }
  }

  // タブの初期化
  document.addEventListener('DOMContentLoaded', function() {
    var triggerTabList = [].slice.call(
      document.querySelectorAll('#mechanismTabs button')
    );
    triggerTabList.forEach(function(triggerEl) {
      var tabTrigger = new bootstrap.Tab(triggerEl);
      triggerEl.addEventListener('click', function(event) {
        event.preventDefault();
        tabTrigger.show();
      });
    });
  });

  // メニュー以外をクリックしたらドロップダウンを閉じる
  document.addEventListener('click', function(event) {
    if (!event.target.closest('.nav-item')) {
      // メニュー以外をクリックしたら全てのnav-itemをinactiveに
      document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
      });
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
  const iframe = document.querySelector('.pdf-container');
      if (iframe) {
          iframe.onload = function () {
              console.log('PDFが正常に読み込まれました');
          };
          iframe.onerror = function () {
              console.error('PDFの読み込みに失敗しました');
          };
      }
  });