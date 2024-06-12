document.addEventListener('DOMContentLoaded', function () {
    // 찜 목록 로드
    loadWishlistFromLocalStorage();

    // 각 체크박스와 모델 목록을 참조
    const hyundaiCheckbox = document.getElementById('hyundai-checkbox');
    const hyundaiModels = document.getElementById('hyundai-models');
    const kiaCheckbox = document.getElementById('kia-checkbox');
    const kiaModels = document.getElementById('kia-models');
    const chevroletCheckbox = document.getElementById('chevrolet-checkbox');
    const chevroletModels = document.getElementById('chevrolet-models');
    const ssangyongCheckbox = document.getElementById('ssangyong-checkbox');
    const ssangyongModels = document.getElementById('ssangyong-models');
    const genesisCheckbox = document.getElementById('genesis-checkbox');
    const genesisModels = document.getElementById('genesis-models');

    // 체크박스를 클릭할 때 모델 목록을 토글하는 함수
    function toggleModels(checkbox, modelsDiv) {
        if (checkbox.checked) {
            modelsDiv.style.display = 'block'; // 체크되면 보이기
        } else {
            modelsDiv.style.display = 'none'; // 체크 해제되면 숨기기
        }
    }

    // 각 제조사 체크박스에 대한 이벤트 리스너 설정
    hyundaiCheckbox.addEventListener('change', function() {
        toggleModels(hyundaiCheckbox, hyundaiModels);
    });
    kiaCheckbox.addEventListener('change', function() {
        toggleModels(kiaCheckbox, kiaModels);
    });
    chevroletCheckbox.addEventListener('change', function() {
        toggleModels(chevroletCheckbox, chevroletModels);
    });
    ssangyongCheckbox.addEventListener('change', function() {
        toggleModels(ssangyongCheckbox, ssangyongModels);
    });
    genesisCheckbox.addEventListener('change', function() {
        toggleModels(genesisCheckbox, genesisModels);
    });

    // 페이지 로드 시 체크박스 상태에 맞게 모델 목록 초기화
    toggleModels(hyundaiCheckbox, hyundaiModels);
    toggleModels(kiaCheckbox, kiaModels);
    toggleModels(chevroletCheckbox, chevroletModels);
    toggleModels(ssangyongCheckbox, ssangyongModels);
    toggleModels(genesisCheckbox, genesisModels);

    // 초기화 버튼 기능
    const resetButtons = document.querySelectorAll('.reset-button');
    resetButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            const section = document.getElementById(target);

            if (section) {
                // 섹션 내의 모든 체크박스와 셀렉트 박스 초기화
                const inputs = section.querySelectorAll('input[type="checkbox"], select');
                inputs.forEach(function(input) {
                    if (input.type === 'checkbox') {
                        input.checked = false;
                    } else if (input.tagName.toLowerCase() === 'select') {
                        input.selectedIndex = 0;
                    }
                });

                // 모델 목록 숨기기
                const modelFilters = section.querySelectorAll('.model-filters');
                modelFilters.forEach(function(modelsDiv) {
                    modelsDiv.style.display = 'none';
                });
            }
        });
    });

    // 사이드바 설정
    setupSidebar(
        'left-sidebar-toggle',
        '.sidebar',
        '250px',
        '10px',
        '←', // 열림 시 아이콘
        '→', // 닫힘 시 아이콘
        'left'
    );

    setupSidebar(
        'right-sidebar-toggle',
        '.right-sidebar',
        '300px',
        '10px',
        '☰', // 열림 시 아이콘
        '☰', // 닫힘 시 아이콘
        'right'
    );

    // 찜 버튼 기능
    setupWishlistButtons();

    // '계산 결과' 버튼 클릭 시 로딩 처리
    document.addEventListener('click', function (event) {
        if (event.target && event.target.classList.contains('calc-button')) {
            event.preventDefault(); // 기본 동작 방지

            const loading = document.getElementById('loading');
            const url = event.target.getAttribute('href'); // 버튼의 href 속성 가져오기

            if (loading) {
                loading.style.display = 'flex'; // 로딩 스피너 표시
            }

            // 10초 후 새 탭을 열기
            setTimeout(() => {
                if (loading) {
                    loading.style.display = 'none'; // 로딩 스피너 숨김
                }

                if (url) {
                    // 새 탭 열기
                    window.open(url, '_blank');
                }
            }, 300); // 10초 후 실행
        }
    });

    // 연식과 주행거리 필터링 적용
    const yearFromSelect = document.getElementById('year-from');
    const yearToSelect = document.getElementById('year-to');
    const distanceFromSelect = document.getElementById('distance-from');
    const distanceToSelect = document.getElementById('distance-to');
    const carListings = document.querySelectorAll('.car-card');

    function applyFilters() {
        const yearFrom = parseInt(yearFromSelect.value, 10) || 0;
        const yearTo = parseInt(yearToSelect.value, 10) || new Date().getFullYear();
        const distanceFrom = parseInt(distanceFromSelect.value, 10) || 0;
        const distanceTo = parseInt(distanceToSelect.value, 10) || Infinity;

        carListings.forEach(car => {
            const carYear = parseInt(car.dataset.year, 10);
            const carMileage = parseInt(car.dataset.mileage, 10);

            if (
                (carYear >= yearFrom && carYear <= yearTo) &&
                (carMileage >= distanceFrom && carMileage <= distanceTo)
            ) {
                car.style.display = 'block';
            } else {
                car.style.display = 'none';
            }
        });
    }

    yearFromSelect.addEventListener('change', applyFilters);
    yearToSelect.addEventListener('change', applyFilters);
    distanceFromSelect.addEventListener('change', applyFilters);
    distanceToSelect.addEventListener('change', applyFilters);

    // 찜 목록 로드 함수
    function loadWishlistFromLocalStorage() {
        const wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
        const wishlistContainer = document.getElementById('wishlist-items');
        wishlistContainer.innerHTML = ''; // 기존 목록 초기화

        wishlist.forEach(item => {
            const listItem = document.createElement('li');
            listItem.setAttribute('data-id', item.id);
            listItem.innerHTML = `
                <div class="wishlist-car-card">
                    <button class="delete-button">X</button>
                    <div class="car-title">${item.title}</div>
                    <div class="car-info">${item.year}년식 | ${item.mileage}</div>
                    <div class="buttons">
                        <a href="${item.detailUrl}" target="_blank" class="button">상세 정보</a>
                        <a href="${item.inspectionUrl}" target="_blank" class="button">검사 정보</a>
                        <a href="${item.calcUrl}" class="button calc-button" target="_blank">가격 예측</a>
                    </div>
                </div>
            `;
            wishlistContainer.appendChild(listItem);

            // 찜 목록에서 제거 기능 추가
            listItem.querySelector('.delete-button').addEventListener('click', function () {
                listItem.remove();
                removeWishlistFromLocalStorage(item.id);

                // 버튼 상태 해제 및 초기 SVG로 변경 (기본 SVG 복원)
                const targetButton = document.querySelector(`.wishlist-button[data-id="${item.id}"]`);
                if (targetButton) {
                    targetButton.classList.remove('active');
                    const originalSVG = targetButton.getAttribute('data-original-svg');
                    targetButton.innerHTML = originalSVG; // 기본 SVG로 복원
                }
            });
        });
    }

    // 찜 버튼 설정 함수
    function setupWishlistButtons() {
        const wishlistButtons = document.querySelectorAll('.wishlist-button');
        const wishlistContainer = document.getElementById('wishlist-items');

        // 각 버튼의 기본 SVG를 data-original-svg에 저장
        wishlistButtons.forEach(button => {
            if (!button.hasAttribute('data-original-svg')) {
                button.setAttribute('data-original-svg', button.innerHTML.trim());
            }
        });

        wishlistButtons.forEach(button => {
            button.addEventListener('click', function () {
                const carId = this.getAttribute('data-id');
                const carTitle = this.getAttribute('data-title');
                const carYear = this.getAttribute('data-year');
                const carMileage = this.getAttribute('data-mileage');
                const carPrice = this.getAttribute('data-price');
                const detailUrl = this.getAttribute('data-detail-url');
                const inspectionUrl = this.getAttribute('data-inspection-url');
                const calcUrl = this.getAttribute('data-calc-url');
                const imageUrl = this.getAttribute('data-image-url');

                // 중복 확인
                if (document.querySelector(`#wishlist-items li[data-id="${carId}"]`)) {
                    alert('이미 찜 목록에 추가된 차량입니다.');
                    return;
                }

                // 버튼 상태 활성화 및 SVG 변경 (찜된 상태)
                this.classList.add('active');
                this.innerHTML = `
                    <svg width="24px" height="24px" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                        <path fill="#F44336" d="M37,43l-13-6l-13,6V9c0-2.2,1.8-4,4-4h18c2.2,0,4,1.8,4,4V43z"/>
                    </svg>
                `;

                // 찜 목록에 추가
                const listItem = document.createElement('li');
                listItem.setAttribute('data-id', carId);
                listItem.innerHTML = `
                    <div class="wishlist-car-card">
                        <button class="delete-button">X</button>
                        <div class="car-title">${carTitle}</div>
                        <div class="car-info">${carYear}년식 | ${carMileage}</div>
                        <div class="buttons">
                            <a href="${detailUrl}" target="_blank" class="button">상세 정보</a>
                            <a href="${inspectionUrl}" target="_blank" class="button">검사 정보</a>
                            <a href="${calcUrl}" class="button calc-button" target="_blank">가격 예측</a>
                        </div>
                    </div>
                `;
                wishlistContainer.appendChild(listItem);

                // 로컬 스토리지에 저장
                saveWishlistToLocalStorage({
                    id: carId,
                    title: carTitle,
                    year: carYear,
                    mileage: carMileage,
                    price: carPrice,
                    detailUrl: detailUrl,
                    inspectionUrl: inspectionUrl,
                    calcUrl: calcUrl,
                    imageUrl: imageUrl
                });

                // 찜 목록에서 제거 기능 추가
                listItem.querySelector('.delete-button').addEventListener('click', function () {
                    listItem.remove();
                    removeWishlistFromLocalStorage(carId);

                    // 버튼 상태 해제 및 초기 SVG로 변경 (기본 SVG 복원)
                    const targetButton = document.querySelector(`.wishlist-button[data-id="${carId}"]`);
                    if (targetButton) {
                        targetButton.classList.remove('active');
                        const originalSVG = targetButton.getAttribute('data-original-svg');
                        targetButton.innerHTML = originalSVG; // 기본 SVG로 복원
                    }
                });
            });
        });

        // 찜 목록 로드 시 버튼 하이라이트 상태 유지 및 제거 기능 설정
        const wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
        wishlist.forEach(item => {
            const button = document.querySelector(`.wishlist-button[data-id="${item.id}"]`);
            if (button) {
                button.classList.add('active');
                button.innerHTML = `
                    <svg width="24px" height="24px" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                        <path fill="#F44336" d="M37,43l-13-6l-13,6V9c0-2.2,1.8-4,4-4h18c2.2,0,4,1.8,4,4V43z"/>
                    </svg>
                `;
            }
        });
    }

    // 찜 목록 저장 함수
    function saveWishlistToLocalStorage(car) {
        let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
        wishlist.push(car);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
    }

    // 찜 목록에서 제거 함수
    function removeWishlistFromLocalStorage(carId) {
        let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
        wishlist = wishlist.filter(item => item.id !== carId);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
    }

    // 사이드바 설정 함수
    function setupSidebar(toggleButtonId, sidebarSelector, openOffset, closedOffset, openIcon, closedIcon, side) {
        const sidebar = document.querySelector(sidebarSelector);
        const toggleButton = document.getElementById(toggleButtonId);
        const content = document.querySelector('.content'); // 추가된 부분

        if (sidebar && toggleButton) {
            toggleButton.addEventListener('click', function () {
                sidebar.classList.toggle('open');

                // 우측 사이드바일 경우 컨텐츠 영역에 클래스 토글
                if (side === 'right' && content) {
                    content.classList.toggle('right-sidebar-open');
                }

                updateToggleButtonPosition();
                toggleArrowIcon();
            });

            document.addEventListener('scroll', updateToggleButtonPosition);
            window.addEventListener('resize', updateToggleButtonPosition);

            function updateToggleButtonPosition() {
                toggleButton.style.position = 'fixed';
                toggleButton.style.top = '5%';
                if (side === 'left') {
                    toggleButton.style.left = sidebar.classList.contains('open') ? openOffset : closedOffset;
                } else {
                    toggleButton.style.right = sidebar.classList.contains('open') ? openOffset : closedOffset;
                }
                toggleButton.style.transform = 'translateY(-50%)';
            }

            function toggleArrowIcon() {
                if (sidebar.classList.contains('open')) {
                    toggleButton.textContent = openIcon;
                } else {
                    toggleButton.textContent = closedIcon;
                }
            }

            // 초기 설정
            updateToggleButtonPosition();
            toggleArrowIcon();
        } else {
            console.error(`${toggleButtonId} 또는 ${sidebarSelector} 요소를 찾을 수 없습니다.`);
        }
    }

    applyFilters();
});
