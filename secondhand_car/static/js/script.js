document.addEventListener('DOMContentLoaded', function () {
    // 찜 목록 로드
    loadWishlistFromLocalStorage();

    // 국내차 토글
    const domesticCheckbox = document.getElementById('domestic-cars');
    const domesticManufacturers = document.getElementById('domestic-manufacturers');

    domesticCheckbox.addEventListener('change', function () {
        if (domesticCheckbox.checked) {
            domesticManufacturers.style.display = 'block';
        } else {
            domesticManufacturers.style.display = 'none';
        }
    });

    if (domesticCheckbox && domesticCheckbox.checked) {
        domesticManufacturers.style.display = 'block';
    } else {
        domesticManufacturers.style.display = 'none';
    }

    // 국내 제조사별 모델 토글 함수
    function toggleModels(checkbox, modelsDiv) {
        if (checkbox && modelsDiv) {
            if (checkbox.checked) {
                modelsDiv.style.display = 'block';
            } else {
                modelsDiv.style.display = 'none';
            }
        }
    }

    const hyundaiCheckbox = document.getElementById('hyundai-checkbox');
    const hyundaiModels = document.getElementById('hyundai-models');
    if (hyundaiCheckbox) {
        hyundaiCheckbox.addEventListener('change', function() {
            toggleModels(hyundaiCheckbox, hyundaiModels);
        });
        toggleModels(hyundaiCheckbox, hyundaiModels);
    }

    const kiaCheckbox = document.getElementById('kia-checkbox');
    const kiaModels = document.getElementById('kia-models');
    if (kiaCheckbox) {
        kiaCheckbox.addEventListener('change', function() {
            toggleModels(kiaCheckbox, kiaModels);
        });
        toggleModels(kiaCheckbox, kiaModels);
    }

    const chevroletCheckbox = document.getElementById('chevrolet-checkbox');
    const chevroletModels = document.getElementById('chevrolet-models');
    if (chevroletCheckbox) {
        chevroletCheckbox.addEventListener('change', function() {
            toggleModels(chevroletCheckbox, chevroletModels);
        });
        toggleModels(chevroletCheckbox, chevroletModels);
    }

    const ssangyongCheckbox = document.getElementById('ssangyong-checkbox');
    const ssangyongModels = document.getElementById('ssangyong-models');
    if (ssangyongCheckbox) {
        ssangyongCheckbox.addEventListener('change', function() {
            toggleModels(ssangyongCheckbox, ssangyongModels);
        });
        toggleModels(ssangyongCheckbox, ssangyongModels);
    }

    const genesisCheckbox = document.getElementById('genesis-checkbox');
    const genesisModels = document.getElementById('genesis-models');
    if (genesisCheckbox) {
        genesisCheckbox.addEventListener('change', function() {
            toggleModels(genesisCheckbox, genesisModels);
        });
        toggleModels(genesisCheckbox, genesisModels);
    }


    // 각 국가별 토글
    const categoryCheckboxes = document.querySelectorAll('.category-filter > input[type="checkbox"]');
    categoryCheckboxes.forEach(categoryCheckbox => {
        const category = categoryCheckbox.value; // 국가 이름 (예: 독일차, 일본차 등)
        const categoryManufacturersDiv = document.getElementById(`${category}-manufacturers`);

        if (categoryCheckbox && categoryManufacturersDiv) {
            categoryCheckbox.addEventListener('change', function () {
                categoryManufacturersDiv.style.display = categoryCheckbox.checked ? 'block' : 'none';
            });

            // 초기 상태 설정
            categoryManufacturersDiv.style.display = categoryCheckbox.checked ? 'block' : 'none';
        }
    });

    // 각 제조사별 모델 토글
    const manufacturerBlocks = document.querySelectorAll('.manufacturer-filter');
    manufacturerBlocks.forEach(block => {
        const checkbox = block.querySelector('input[type="checkbox"]'); // 제조사 체크박스
        const modelsDiv = block.querySelector('.model-filters'); // 해당 제조사의 모델 목록

        if (checkbox && modelsDiv) {
            checkbox.addEventListener('change', function () {
                modelsDiv.style.display = checkbox.checked ? 'block' : 'none';
            });

            // 초기 상태 설정
            modelsDiv.style.display = checkbox.checked ? 'block' : 'none';
        }
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
        '270px',
        '10px',
        '☰', // 열림 시 아이콘
        '☰', // 닫힘 시 아이콘
        'right'
    );

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

            // 3초 후 새 탭을 열기
            setTimeout(() => {
                if (loading) {
                    loading.style.display = 'none'; // 로딩 스피너 숨김
                }

                if (url) {
                    // 새 탭 열기
                    window.open(url, '_blank');
                }
            }, 3000);
        }
    });

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

                // 버튼 상태 해제 및 원래 SVG로 복원
                const targetButton = document.querySelector(`.wishlist-button[data-id="${item.id}"]`);
                if (targetButton) {
                    targetButton.classList.remove('active');
                    const originalSVG = targetButton.getAttribute('data-original-svg');
                    targetButton.innerHTML = originalSVG;
                }
            });
        });
    }

    function setupWishlistButtons() {
        const wishlistButtons = document.querySelectorAll('.wishlist-button');
        const wishlistContainer = document.getElementById('wishlist-items');

        // 각 버튼의 기본 SVG 저장
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

                // 버튼 상태 활성화 및 SVG 변경
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

                // 찜 목록에서 제거 기능
                listItem.querySelector('.delete-button').addEventListener('click', function () {
                    listItem.remove();
                    removeWishlistFromLocalStorage(carId);

                    // 버튼 상태 해제 및 원래 SVG 복원
                    const targetButton = document.querySelector(`.wishlist-button[data-id="${carId}"]`);
                    if (targetButton) {
                        targetButton.classList.remove('active');
                        const originalSVG = targetButton.getAttribute('data-original-svg');
                        targetButton.innerHTML = originalSVG;
                    }
                });
            });
        });

        // 찜 목록 로드 시 버튼 상태 유지
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

    function saveWishlistToLocalStorage(car) {
        let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
        wishlist.push(car);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
    }

    function removeWishlistFromLocalStorage(carId) {
        let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
        wishlist = wishlist.filter(item => item.id !== carId);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
    }

    function setupSidebar(toggleButtonId, sidebarSelector, openOffset, closedOffset, openIcon, closedIcon, side) {
        const sidebar = document.querySelector(sidebarSelector);
        const toggleButton = document.getElementById(toggleButtonId);
        const content = document.querySelector('.content');

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

    // 색상 필터 "더 보기" 버튼 기능 수정
    const toggleColorsButton = document.getElementById('toggle-colors');
    const colorFilter = document.querySelector('.color-filter');

    if (toggleColorsButton && colorFilter) {
        toggleColorsButton.addEventListener('click', function () {
            if (colorFilter.classList.contains('expanded')) {
                colorFilter.classList.remove('expanded');
                toggleColorsButton.textContent = '더 보기';
            } else {
                colorFilter.classList.add('expanded');
                toggleColorsButton.textContent = '접기';
            }
        });
    } else {
        console.error('toggle-colors 버튼 또는 color-filter 요소를 찾을 수 없습니다.');
    }

    // 색상 선택 기능 추가
    const colorOptions = document.querySelectorAll('.color-option');
    const selectedColorsInputs = document.getElementById('selected-colors-inputs');

    colorOptions.forEach(option => {
        option.addEventListener('click', function () {
            this.classList.toggle('selected');
            const color = this.getAttribute('data-color');

            if (this.classList.contains('selected')) {
                // 선택된 색상을 숨겨진 입력 필드에 추가
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'color';
                input.value = color;
                input.setAttribute('data-color', color);
                selectedColorsInputs.appendChild(input);
            } else {
                // 선택 해제된 색상의 숨겨진 입력 필드 제거
                const inputToRemove = selectedColorsInputs.querySelector(`input[data-color="${color}"]`);
                if (inputToRemove) {
                    selectedColorsInputs.removeChild(inputToRemove);
                }
            }
        });
    });

    // 초기 선택 상태 설정
    const initialSelectedColors = selectedColorsInputs.querySelectorAll('input[name="color"]');
    initialSelectedColors.forEach(input => {
        const color = input.value;
        const correspondingOption = document.querySelector(`.color-option[data-color="${color}"]`);
        if (correspondingOption) {
            correspondingOption.classList.add('selected');
        }
    });
document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('floating-search-button');
    const manufacturerSections = document.querySelectorAll('.manufacturer-filter');

    manufacturerSections.forEach(section => {
        const checkbox = section.querySelector('input[type="checkbox"]');
        const modelsDiv = section.querySelector('.model-filters');

        if (checkbox && modelsDiv) {
            checkbox.addEventListener('change', function () {
                // 모델 목록이 열리거나 닫힐 때 버튼 위치를 업데이트
                updateSearchButtonPosition();
            });
        }
    });

    function updateSearchButtonPosition() {
        let totalHeight = 0;
        const openSections = document.querySelectorAll('.manufacturer-filter .model-filters');

        // 열려 있는 모든 모델 필터 섹션의 높이를 계산
        openSections.forEach(modelsDiv => {
            if (modelsDiv.style.display === 'block') {
                totalHeight += modelsDiv.offsetHeight;
            }
        });

        // 버튼 위치 조정
        if (searchButton) {
            searchButton.style.bottom = `${20 + totalHeight}px`; // 기본 하단 + 추가 높이
        }
    }

    // 초기 상태 업데이트
    updateSearchButtonPosition();
});
});