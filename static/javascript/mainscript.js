// ドロップダウンメニューの開閉
function toggleDropdown(element) {
    const activeClass = 'active';
    const isActive = element.classList.contains(activeClass);

    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove(activeClass);
    });

    if (!isActive) {
        element.classList.add(activeClass);
    }
}

// メニュー以外をクリックしたら閉じる
document.addEventListener('click', (event) => {
    const isClickInside = event.target.closest('.nav-item');
    if (!isClickInside) {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
    }
});

// チェックボックス変更時にフォームを自動送信
function submitForm() {
    const details = document.getElementById('mechanism-details');
    const wasOpen = details.open;

    const form = document.getElementById('search-form');
    form.submit();

    if (wasOpen) {
        details.setAttribute('open', 'true');
    }
}

// だおだおテキスト開閉ボタン
function toggleDaodaoText() {
    const daodaoText = document.getElementById('daodao-text');
    if (daodaoText.style.display === '' || daodaoText.style.display === 'none') {
        daodaoText.style.display = 'block';
    } else {
        daodaoText.style.display = 'none';
    }
}

// スライドショー
document.addEventListener("DOMContentLoaded", () => {
    const slides = document.querySelectorAll(".img-slide");
    const slideLinks = document.querySelectorAll(".img-slide-link");
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle("active", i === index);
        });
        slideLinks.forEach((link, i) => {
            link.style.pointerEvents = i === index ? "auto" : "none"; // Only the active slide is clickable
            link.style.opacity = i === index ? "1" : "0"; // Show only the active link
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    showSlide(currentSlide);

    setInterval(nextSlide, 5000);
});

function clearAllCheckboxes() {
    const checkboxes = document.querySelectorAll('input[name="mechanisms"]');

    checkboxes.forEach(checkbox => checkbox.checked = false);
    
    document.getElementById('search-form').submit();
}

document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            const textId = button.getAttribute('data-text-id');
            try {
                const response = await fetch(`/like/${textId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    const likesElement = document.getElementById(`likes-${textId}`);
                    likesElement.innerText = data.likes;
                } else {
                    console.error('いいねの送信に失敗しました。');
                }
            } catch (error) {
                console.error('通信エラーが発生しました:', error);
            }
        });
    });
});
