document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll('.entry-content img, .comment-content img');
    let currentZoom = null;

    images.forEach(img => {
        img.classList.add('zoomable');

        img.addEventListener('click', function (e) {
            e.stopPropagation();

            if (currentZoom) {
                currentZoom.click();
                return;
            }

            const rect = img.getBoundingClientRect();
            const naturalWidth = img.naturalWidth;
            const naturalHeight = img.naturalHeight;

            const clone = img.cloneNode();
            clone.classList.add('zoom-overlay');
            clone.style.left = `${rect.left}px`;
            clone.style.top = `${rect.top}px`;
            clone.style.width = `${rect.width}px`;
            clone.style.height = `${rect.height}px`;
            clone.style.transform = 'scale(1)';

            document.body.appendChild(clone);
            currentZoom = clone;

            // 强制 reflow
            clone.offsetWidth;

            // 计算目标宽高
            const maxWidth = window.innerWidth * 0.9;
            const maxHeight = window.innerHeight * 0.9;
            let targetWidth = naturalWidth;
            let targetHeight = naturalHeight;

            if (naturalWidth > maxWidth || naturalHeight > maxHeight) {
                const ratio = Math.min(maxWidth / naturalWidth, maxHeight / naturalHeight);
                targetWidth = naturalWidth * ratio;
                targetHeight = naturalHeight * ratio;
            }

            const targetLeft = (window.innerWidth - targetWidth) / 2;
            const targetTop = (window.innerHeight - targetHeight) / 2;

            // 应用目标位置和尺寸
            clone.style.left = `${targetLeft}px`;
            clone.style.top = `${targetTop}px`;
            clone.style.width = `${targetWidth}px`;
            clone.style.height = `${targetHeight}px`;

            // 添加放大回弹效果
            clone.style.transform = 'scale(1.05)';
            setTimeout(() => {
                clone.style.transform = 'scale(1)';
            }, 100); // 回弹时间

            // 点击关闭
            clone.addEventListener('click', function () {
                // 添加缩小回弹效果
                clone.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    clone.style.transform = 'scale(1)';
                }, 100);

                // 回退到原始位置和尺寸
                clone.style.left = `${rect.left}px`;
                clone.style.top = `${rect.top}px`;
                clone.style.width = `${rect.width}px`;
                clone.style.height = `${rect.height}px`;

                // 等动画结束再移除
                setTimeout(() => {
                    if (clone.parentNode) {
                        clone.parentNode.removeChild(clone);
                        currentZoom = null;
                    }
                }, 400);
            });
        });
    });

    document.addEventListener('click', function () {
        if (currentZoom) {
            currentZoom.click();
        }
    });

    // 添加 Esc 键关闭功能
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && currentZoom) {
            currentZoom.click();
        }
    });
});