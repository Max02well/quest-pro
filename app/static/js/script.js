<script>
document.addEventListener("DOMContentLoaded", () => {
    const jobGrid = document.getElementById("job-grid");
    const searchButton = document.getElementById("search-button");
    const loadingElement = document.getElementById("loading");
    const noResultsElement = document.getElementById("no-results");
    const paginationContainer = document.getElementById("pagination");
    const mobileFilterToggle = document.getElementById("mobile-filter-toggle");
    const filterContainer = document.getElementById("filter-container");
    const copyrightYear = document.getElementById("copyright-year");
    const JOBS_PER_PAGE = 3;

    let currentState = {
        page: 1,
        totalPages: 1,
        searchParams: new URLSearchParams(window.location.search)
    };

    // Elements cache
    const filters = {
        keyword: document.getElementById("keyword-input"),
        location: document.getElementById("location-input"),
        jobType: document.getElementById("job-type-filter"),
        experience: document.getElementById("experience-filter"),
        salary: document.getElementById("salary-filter")
    };

    // State initialization
    function initializeState() {
        currentState.page = parseInt(currentState.searchParams.get('page')) || 1;
        Object.entries(filters).forEach(([key, element]) => {
            element.value = currentState.searchParams.get(key) || '';
        });
    }

    // Loading states
    const loadingState = {
        show: () => {
            loadingElement.classList.add("active");
            jobGrid.style.display = "none";
            noResultsElement.classList.remove("active");
            paginationContainer.style.visibility = "hidden";
        },
        hide: () => {
            loadingElement.classList.remove("active");
            jobGrid.style.display = "grid";
            paginationContainer.style.visibility = "visible";
        }
    };

    // Mobile filter toggle functionality
    function setupMobileToggle() {
        if (mobileFilterToggle && filterContainer) {
            mobileFilterToggle.addEventListener("click", () => {
                filterContainer.classList.toggle("active");
                mobileFilterToggle.textContent = filterContainer.classList.contains("active") ? "Hide Filters" : "Show Filters";
            });
        }
    }

    // Update copyright year dynamically
    function updateCopyrightYear() {
        if (copyrightYear) {
            copyrightYear.textContent = new Date().getFullYear();
        }
    }

    // Data fetching
    async function fetchJobs() {
        try {
            loadingState.show();

            const params = new URLSearchParams({
                keyword: filters.keyword.value,
                location: filters.location.value,
                type: filters.jobType.value,
                experience: filters.experience.value,
                salaryRange: filters.salary.value,
                page: currentState.page
            });

            const response = await fetch(`/jobs/explore?${params.toString()}`);

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const { jobs, total, pages } = await response.json();

            currentState.totalPages = pages;
            renderJobs(jobs);
            renderPagination(pages);
            updateBrowserHistory(params);

        } catch (error) {
            console.error('Fetch error:', error);
            showErrorState();
        } finally {
            loadingState.hide();
        }
    }

    // Event handlers
    function setupEventListeners() {
        searchButton.addEventListener("click", () => {
            currentState.page = 1;
            fetchJobs();
        });

        Object.values(filters).forEach(filter => {
            if (filter.tagName === 'SELECT') {
                filter.addEventListener("change", () => {
                    currentState.page = 1;
                    fetchJobs();
                });
            } else {
                filter.addEventListener("keyup", debounce(() => {
                    currentState.page = 1;
                    fetchJobs();
                }, 300));
            }
        });

        window.addEventListener('popstate', () => {
            currentState.searchParams = new URLSearchParams(window.location.search);
            initializeState();
            fetchJobs();
        });
    }

    // Initialization
    initializeState();
    setupEventListeners();
    setupMobileToggle();
    fetchJobs();
    updateCopyrightYear();
});
</script>
