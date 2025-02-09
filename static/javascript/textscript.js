// ドロップダウンメニュー：クリックで表示/非表示を切り替え
function toggleDropdown(element) {
  // 他のnav-itemを一旦閉じる
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
  const triggerTabList = [].slice.call(
      document.querySelectorAll('#mechanismTabs button')
  );
  triggerTabList.forEach(function(triggerEl) {
      const tabTrigger = new bootstrap.Tab(triggerEl);
      triggerEl.addEventListener('click', function(event) {
          event.preventDefault();
          tabTrigger.show();
      });
  });
});

// メニュー以外をクリックしたらドロップダウンを閉じる
document.addEventListener('click', function(event) {
  if (!event.target.closest('.nav-item')) {
      // メニュー以外をクリックしたら全てのnav-itemを非アクティブに
      document.querySelectorAll('.nav-item').forEach(item => {
          item.classList.remove('active');
      });
  }
});

// PDF読み込みイベントの監視
document.addEventListener('DOMContentLoaded', function() {
  const iframe = document.querySelector('.pdf-container');
  if (iframe) {
      iframe.onload = function() {
          console.log('PDFが正常に読み込まれました');
      };
      iframe.onerror = function() {
          console.error('PDFの読み込みに失敗しました');
      };
  }
});

document.addEventListener("DOMContentLoaded", () => {
    // すべての「いいねボタン」を取得
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const textId = button.dataset.textId;

            // いいね数を取得
            const likesCountElement = document.getElementById(`likes-${textId}`);
            let likesCount = parseInt(likesCountElement.textContent, 10);

            // いいね数を1増加
            likesCount++;
            likesCountElement.textContent = likesCount;

            // サーバーにいいね数を送信
            fetch(`/like/${textId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ likes: likesCount }),
            })
            .then((response) => {
                if (!response.ok) {
                    console.error("Error updating likes");
                }
            })
            .catch((error) => {
                console.error("Network error:", error);
            });
        });
    });
});
