/** @type {import('next').NextConfig} */
const nextConfig = {
    typescript: {
        ignoreBuildErrors: true,
    },
    // 这行代码配置了Next.js的输出模式为静态导出模式
    // 当设置为'export'时，Next.js会生成静态HTML文件
    // 适用于不需要服务端渲染的纯静态网站
    // 与capacitor.config.ts中的webDir配置配合使用
    // 可以将生成的静态文件部署到任何静态托管服务
    output: 'export',
};

export default nextConfig;
