/*
 * Project: ArXiv_AcceleratorPhysics
 * File: app.js  
 * Author: Ming Liu (ming-1018@foxmail.com)
 * Institution: Institute of High Energy Physics, Chinese Academy of Sciences
 * Created: July 25th, 2025
 * Description: Web界面核心JavaScript库
 *
 * 功能模块:
 * - API客户端封装
 * - 图表管理系统
 * - 状态管理器
 * - 工具函数库
 * - 实时数据更新
 *
 * 技术栈:
 * - 原生JavaScript (ES6+)
 * - Chart.js图表库
 * - Bootstrap 5组件
 * - 异步API调用
 *
 * Version: 1.1.0
 */

// ArXiv分析系统Web界面JavaScript

// 全局配置
const AppConfig = {
    apiBaseUrl: '/api',
    refreshInterval: 30000, // 30秒
    chartColors: {
        primary: '#007bff',
        success: '#28a745',
        warning: '#ffc107',
        danger: '#dc3545',
        info: '#17a2b8'
    }
};

// 工具函数
const Utils = {
    // 格式化日期
    formatDate: (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN');
    },

    // 格式化数字
    formatNumber: (num) => {
        return new Intl.NumberFormat('zh-CN').format(num);
    },

    // 显示加载状态
    showLoading: (element, text = '加载中...') => {
        if (element) {
            element.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border spinner-border-sm me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    ${text}
                </div>
            `;
        }
    },

    // 显示错误信息
    showError: (message, type = 'danger') => {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        const container = document.querySelector('.container-fluid') || document.body;
        container.insertAdjacentHTML('afterbegin', alertHtml);
    },

    // 显示成功信息
    showSuccess: (message) => {
        Utils.showError(message, 'success');
    },

    // 防抖函数
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // 节流函数
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// API调用类
class ApiClient {
    constructor(baseUrl = AppConfig.apiBaseUrl) {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // 获取统计数据
    async getStats() {
        return this.request('/stats');
    }

    // 启动分析任务
    async runAnalysis(forceUpdate = false) {
        return this.request('/run_analysis', {
            method: 'POST',
            body: JSON.stringify({ force_update: forceUpdate })
        });
    }

    // 获取分析状态
    async getAnalysisStatus() {
        return this.request('/analysis_status');
    }
}

// 图表管理类
class ChartManager {
    constructor() {
        this.charts = {};
    }

    // 创建趋势图表
    createTrendChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels || [],
                datasets: [{
                    label: '论文数量',
                    data: data.values || [],
                    borderColor: AppConfig.chartColors.primary,
                    backgroundColor: AppConfig.chartColors.primary + '20',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    // 创建饼图
    createPieChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }

        this.charts[canvasId] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels || [],
                datasets: [{
                    data: data.values || [],
                    backgroundColor: [
                        AppConfig.chartColors.primary,
                        AppConfig.chartColors.success,
                        AppConfig.chartColors.warning,
                        AppConfig.chartColors.danger,
                        AppConfig.chartColors.info
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        return this.charts[canvasId];
    }

    // 销毁图表
    destroyChart(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
    }

    // 销毁所有图表
    destroyAll() {
        Object.keys(this.charts).forEach(id => {
            this.destroyChart(id);
        });
    }
}

// 状态管理类
class StateManager {
    constructor() {
        this.state = {
            analysisStatus: 'idle',
            lastUpdate: null,
            stats: {}
        };
        this.listeners = {};
    }

    // 添加状态监听器
    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    }

    // 移除状态监听器
    off(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        }
    }

    // 触发事件
    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => callback(data));
        }
    }

    // 更新状态
    setState(newState) {
        const prevState = { ...this.state };
        this.state = { ...this.state, ...newState };
        this.emit('stateChange', { prevState, newState: this.state });
    }

    // 获取状态
    getState() {
        return { ...this.state };
    }
}

// 主应用类
class ArxivApp {
    constructor() {
        this.api = new ApiClient();
        this.chartManager = new ChartManager();
        this.stateManager = new StateManager();
        this.refreshTimer = null;

        this.init();
    }

    // 初始化应用
    async init() {
        this.bindEvents();
        this.startAutoRefresh();
        
        // 页面特定初始化
        const currentPage = this.getCurrentPage();
        switch (currentPage) {
            case 'index':
                await this.initHomePage();
                break;
            case 'statistics':
                await this.initStatisticsPage();
                break;
            case 'analysis':
                await this.initAnalysisPage();
                break;
        }
    }

    // 获取当前页面
    getCurrentPage() {
        const path = window.location.pathname;
        if (path === '/') return 'index';
        if (path.includes('/statistics')) return 'statistics';
        if (path.includes('/analysis')) return 'analysis';
        if (path.includes('/papers')) return 'papers';
        if (path.includes('/config')) return 'config';
        return 'unknown';
    }

    // 绑定事件
    bindEvents() {
        // 监听状态变化
        this.stateManager.on('stateChange', (data) => {
            this.onStateChange(data);
        });

        // 窗口关闭前清理
        window.addEventListener('beforeunload', () => {
            this.cleanup();
        });

        // 处理网络状态变化
        window.addEventListener('online', () => {
            Utils.showSuccess('网络连接已恢复');
            this.startAutoRefresh();
        });

        window.addEventListener('offline', () => {
            Utils.showError('网络连接已断开', 'warning');
            this.stopAutoRefresh();
        });
    }

    // 状态变化处理
    onStateChange(data) {
        const { newState } = data;
        
        // 更新分析状态显示
        const statusElement = document.getElementById('analysis-status');
        if (statusElement) {
            const statusMap = {
                'idle': { text: '就绪', class: 'bg-success' },
                'running': { text: '运行中', class: 'bg-warning' },
                'completed': { text: '完成', class: 'bg-success' },
                'error': { text: '错误', class: 'bg-danger' }
            };
            
            const status = statusMap[newState.analysisStatus] || statusMap['idle'];
            statusElement.textContent = status.text;
            statusElement.className = 'badge ' + status.class;
        }
    }

    // 初始化首页
    async initHomePage() {
        try {
            // 加载统计数据
            const stats = await this.api.getStats();
            this.stateManager.setState({ stats });

            // 初始化趋势图表
            this.initTrendChart();

            // 更新分析状态
            await this.updateAnalysisStatus();
        } catch (error) {
            console.error('首页初始化失败:', error);
        }
    }

    // 初始化统计页面
    async initStatisticsPage() {
        try {
            const stats = await this.api.getStats();
            this.stateManager.setState({ stats });

            // 初始化各种图表
            this.initStatisticsCharts();
        } catch (error) {
            console.error('统计页面初始化失败:', error);
        }
    }

    // 初始化分析页面
    async initAnalysisPage() {
        try {
            await this.updateAnalysisStatus();
        } catch (error) {
            console.error('分析页面初始化失败:', error);
        }
    }

    // 初始化趋势图表
    initTrendChart() {
        // 生成模拟数据
        const labels = [];
        const values = [];
        
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }));
            values.push(Math.floor(Math.random() * 10) + 1);
        }

        this.chartManager.createTrendChart('trendChart', { labels, values });
    }

    // 初始化统计图表
    initStatisticsCharts() {
        // 分类分布图表
        const categoryData = {
            labels: ['加速器', '束流物理', '模拟计算', '仪器设备', '其他'],
            values: [30, 25, 20, 15, 10]
        };
        this.chartManager.createPieChart('categoryChart', categoryData);

        // 时间趋势图表
        this.initTrendChart();
    }

    // 更新分析状态
    async updateAnalysisStatus() {
        try {
            const status = await this.api.getAnalysisStatus();
            this.stateManager.setState({ 
                analysisStatus: status.status,
                lastUpdate: new Date().toISOString()
            });
        } catch (error) {
            console.error('获取分析状态失败:', error);
        }
    }

    // 启动分析任务
    async runAnalysis(forceUpdate = false) {
        try {
            this.stateManager.setState({ analysisStatus: 'running' });
            
            const result = await this.api.runAnalysis(forceUpdate);
            
            if (result.success) {
                Utils.showSuccess('分析任务已启动');
                // 开始轮询状态
                this.pollAnalysisStatus();
            } else {
                throw new Error(result.message || '启动失败');
            }
        } catch (error) {
            this.stateManager.setState({ analysisStatus: 'error' });
            Utils.showError('启动分析失败: ' + error.message);
        }
    }

    // 轮询分析状态
    pollAnalysisStatus() {
        const poll = async () => {
            try {
                const status = await this.api.getAnalysisStatus();
                this.stateManager.setState({ analysisStatus: status.status });
                
                if (status.status === 'running') {
                    setTimeout(poll, 5000); // 5秒后再次检查
                }
            } catch (error) {
                console.error('轮询状态失败:', error);
            }
        };
        
        setTimeout(poll, 5000);
    }

    // 开始自动刷新
    startAutoRefresh() {
        this.stopAutoRefresh(); // 确保没有重复的定时器
        
        this.refreshTimer = setInterval(async () => {
            if (navigator.onLine) {
                await this.updateAnalysisStatus();
            }
        }, AppConfig.refreshInterval);
    }

    // 停止自动刷新
    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }

    // 清理资源
    cleanup() {
        this.stopAutoRefresh();
        this.chartManager.destroyAll();
    }
}

// 全局函数
window.runAnalysis = function(forceUpdate = false) {
    if (window.arxivApp) {
        window.arxivApp.runAnalysis(forceUpdate);
    }
};

window.updateAnalysisStatus = function() {
    if (window.arxivApp) {
        window.arxivApp.updateAnalysisStatus();
    }
};

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', function() {
    // 初始化应用
    window.arxivApp = new ArxivApp();
    
    // 初始化Bootstrap组件
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// 导出供其他模块使用
window.ArxivApp = {
    Utils,
    ApiClient,
    ChartManager,
    StateManager
};
