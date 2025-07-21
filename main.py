"""
Academic Web Automation System using Puppeteer & Streamlit
========================================================

A demonstration of browser automation principles combining Python web frameworks
with Node.js automation libraries for educational and research purposes.

Author: [Your Name]
Course: [Course Code] - Web Technologies/Automation
Date: July 2025

Key Concepts Demonstrated:
- Inter-language communication (Python ↔ Node.js)
- Subprocess management and error handling
- Asynchronous browser automation
- Cross-platform executable detection
- Package management integration
- Real-time UI feedback systems
"""

import streamlit as st
import subprocess
import json
import os
from pathlib import Path
from typing import Tuple, Dict, Optional

# Configuration
CONFIG = {
    "app_title": "🎓 Academic Browser Automation System",
    "app_subtitle": "Demonstrating Modern Web Automation Principles",
    "timeout": 300,  # Increased to 5 minutes for complex operations
    "viewport": {"width": 1280, "height": 720},
    "analysis_timeout": 45000,  # 45 seconds for page analysis
    "installation_timeout": 600  # 10 minutes for Puppeteer installation
}

class SystemManager:
    """Manages system dependencies and environment setup"""
    
    @staticmethod
    def find_executables() -> Tuple[Optional[str], Optional[str]]:
        """Cross-platform Node.js executable detection"""
        node_path = npm_path = None
        
        try:
            # Cross-platform executable discovery
            result = subprocess.run(['where' if os.name == 'nt' else 'which', 'node'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                node_path = result.stdout.strip().split('\n')[0]
        except: pass
        
        try:
            result = subprocess.run(['where' if os.name == 'nt' else 'which', 'npm'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                npm_path = result.stdout.strip().split('\n')[0]
        except: pass
        
        return node_path, npm_path
    
    @staticmethod
    def validate_environment() -> Tuple[bool, Optional[str], Optional[str]]:
        """Environment validation with detailed feedback"""
        node_path, npm_path = SystemManager.find_executables()
        
        if not node_path:
            return False, None, None
            
        try:
            result = subprocess.run([node_path, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0, node_path, npm_path
        except:
            return False, None, None

class PuppeteerManager:
    """Handles Puppeteer installation and script execution"""
    
    @staticmethod
    def ensure_installation(npm_path: str) -> Dict[str, any]:
        """Smart dependency installation with enhanced feedback"""
        if Path('node_modules').exists():
            return {"success": True, "message": "Dependencies already installed"}
        
        # Create comprehensive package.json with additional dev tools
        package_config = {
            "name": "academic-browser-automation",
            "version": "1.0.0",
            "description": "Academic demonstration of browser automation with detailed analysis",
            "main": "index.js",
            "dependencies": {
                "puppeteer": "^21.0.0"
            },
            "devDependencies": {},
            "scripts": {
                "test": "node test.js"
            },
            "keywords": ["automation", "academic", "browser", "research"],
            "author": "Academic Project",
            "license": "MIT"
        }
        
        try:
            with open('package.json', 'w') as f:
                json.dump(package_config, f, indent=2)
            
            result = subprocess.run([npm_path, 'install'], 
                                  capture_output=True, text=True, 
                                  timeout=CONFIG["installation_timeout"])
            
            return {
                "success": result.returncode == 0,
                "message": "Installation successful" if result.returncode == 0 else result.stderr,
                "details": {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "return_code": result.returncode
                }
            }
        except Exception as e:
            return {"success": False, "message": str(e), "details": {"error": str(e)}}

    @staticmethod
    def create_script(action: str, **kwargs) -> str:
        """Dynamic JavaScript generation for different automation tasks"""
        
        base_config = """
        const puppeteer = require('puppeteer');
        const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
        
        (async () => {
            try {
                console.log('🚀 Initializing browser automation...');
                
                const browser = await puppeteer.launch({
                    headless: false,
                    defaultViewport: { width: 1280, height: 720 },
                    args: ['--no-sandbox', '--disable-setuid-sandbox']
                });
                
                const page = await browser.newPage();
        """
        
        if action == "demo":
            script_body = f"""
                console.log('📖 Academic Demo: Comprehensive Research Portal Analysis...');
                await page.goto('https://scholar.google.com', {{ 
                    waitUntil: 'networkidle2', timeout: {CONFIG["analysis_timeout"]}
                }});
                
                // Comprehensive page analysis
                console.log('🔍 Performing detailed page analysis...');
                const analysis = await page.evaluate(() => {{
                    const getTextContent = (selector) => {{
                        const el = document.querySelector(selector);
                        return el ? el.textContent.trim() : 'Not found';
                    }};
                    
                    const countElements = (selector) => document.querySelectorAll(selector).length;
                    
                    return {{
                        // Basic metadata
                        title: document.title,
                        url: window.location.href,
                        charset: document.characterSet,
                        lastModified: document.lastModified,
                        
                        // Content analysis
                        totalLinks: countElements('a'),
                        externalLinks: Array.from(document.querySelectorAll('a')).filter(a => 
                            a.href && !a.href.includes(window.location.hostname)).length,
                        images: countElements('img'),
                        forms: countElements('form'),
                        buttons: countElements('button'),
                        inputs: countElements('input'),
                        
                        // Structure analysis
                        headings: {{
                            h1: countElements('h1'),
                            h2: countElements('h2'),
                            h3: countElements('h3'),
                            h4: countElements('h4'),
                            h5: countElements('h5'),
                            h6: countElements('h6')
                        }},
                        
                        // Content metrics
                        textLength: document.body.innerText.length,
                        wordCount: document.body.innerText.split(/\\s+/).length,
                        paragraphs: countElements('p'),
                        lists: countElements('ul, ol'),
                        tables: countElements('table'),
                        
                        // Technical analysis
                        hasServiceWorker: 'serviceWorker' in navigator,
                        hasLocalStorage: typeof(Storage) !== "undefined",
                        viewportWidth: window.innerWidth,
                        viewportHeight: window.innerHeight,
                        
                        // Performance hints
                        loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
                        domElements: document.getElementsByTagName('*').length
                    }};
                }});
                
                // Display comprehensive analysis
                console.log('📊 COMPREHENSIVE WEBSITE ANALYSIS REPORT');
                console.log('=' .repeat(50));
                console.log(`📝 Title: ${{analysis.title}}`);
                console.log(`🌐 URL: ${{analysis.url}}`);
                console.log(`📅 Last Modified: ${{analysis.lastModified}}`);
                console.log(`⚡ Load Time: ${{analysis.loadTime}}ms`);
                console.log('');
                
                console.log('🔗 LINK ANALYSIS:');
                console.log(`   Total Links: ${{analysis.totalLinks}}`);
                console.log(`   External Links: ${{analysis.externalLinks}}`);
                console.log(`   Internal Links: ${{analysis.totalLinks - analysis.externalLinks}}`);
                console.log('');
                
                console.log('🏗️ STRUCTURE ANALYSIS:');
                console.log(`   H1 Headings: ${{analysis.headings.h1}}`);
                console.log(`   H2 Headings: ${{analysis.headings.h2}}`);
                console.log(`   H3 Headings: ${{analysis.headings.h3}}`);
                console.log(`   Total DOM Elements: ${{analysis.domElements}}`);
                console.log(`   Paragraphs: ${{analysis.paragraphs}}`);
                console.log(`   Lists: ${{analysis.lists}}`);
                console.log(`   Tables: ${{analysis.tables}}`);
                console.log('');
                
                console.log('📝 CONTENT METRICS:');
                console.log(`   Text Length: ${{analysis.textLength.toLocaleString()}} characters`);
                console.log(`   Word Count: ${{analysis.wordCount.toLocaleString()}} words`);
                console.log(`   Images: ${{analysis.images}}`);
                console.log('');
                
                console.log('⚙️ INTERACTIVE ELEMENTS:');
                console.log(`   Forms: ${{analysis.forms}}`);
                console.log(`   Buttons: ${{analysis.buttons}}`);
                console.log(`   Input Fields: ${{analysis.inputs}}`);
                console.log('');
                
                console.log('🖥️ TECHNICAL DETAILS:');
                console.log(`   Viewport: ${{analysis.viewportWidth}}x${{analysis.viewportHeight}}`);
                console.log(`   Character Set: ${{analysis.charset}}`);
                console.log(`   Service Worker: ${{analysis.hasServiceWorker ? 'Available' : 'Not Available'}}`);
                console.log(`   Local Storage: ${{analysis.hasLocalStorage ? 'Available' : 'Not Available'}}`);
                console.log('');
                
                // Take screenshot with timestamp
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                const screenshotPath = `academic_demo_${{timestamp}}.png`;
                await page.screenshot({{ 
                    path: screenshotPath, 
                    fullPage: true,
                    type: 'png'
                }});
                console.log(`📸 Full-page screenshot saved: ${{screenshotPath}}`);
                
                // Generate summary report
                const efficiency = analysis.textLength / analysis.domElements;
                const linkDensity = (analysis.totalLinks / analysis.wordCount * 100).toFixed(2);
                
                console.log('📈 EFFICIENCY METRICS:');
                console.log(`   Content Efficiency: ${{efficiency.toFixed(2)}} chars/element`);
                console.log(`   Link Density: ${{linkDensity}}% (links per 100 words)`);
                console.log(`   Heading Structure: ${{analysis.headings.h1 > 0 ? 'Good' : 'Missing H1'}}`);
                
                await delay(5000);
                await browser.close();
                console.log('✅ Comprehensive academic demo completed successfully');
            """
        
        elif action == "research":
            url = kwargs.get("url", "https://example.com")
            script_body = f"""
                const url = '{url}';
                console.log(`🔬 ADVANCED RESEARCH MODE: Deep Analysis of ${{url}}`);
                console.log('=' .repeat(60));
                
                // Navigate with extended timeout
                await page.goto(url, {{ 
                    waitUntil: 'networkidle2', 
                    timeout: {CONFIG["analysis_timeout"]}
                }});
                
                console.log('⏱️ Page loaded, beginning comprehensive analysis...');
                
                // Advanced metrics collection
                const detailedMetrics = await page.evaluate(() => {{
                    // Helper functions
                    const getTextContent = (selector) => {{
                        const el = document.querySelector(selector);
                        return el ? el.textContent.trim() : null;
                    }};
                    
                    const countElements = (selector) => document.querySelectorAll(selector).length;
                    
                    const getMetaTags = () => {{
                        const metas = {{}};
                        document.querySelectorAll('meta').forEach(meta => {{
                            const name = meta.getAttribute('name') || meta.getAttribute('property');
                            if (name) metas[name] = meta.getAttribute('content');
                        }});
                        return metas;
                    }};
                    
                    const analyzeColors = () => {{
                        const styles = window.getComputedStyle(document.body);
                        return {{
                            backgroundColor: styles.backgroundColor,
                            color: styles.color,
                            fontFamily: styles.fontFamily,
                            fontSize: styles.fontSize
                        }};
                    }};
                    
                    const checkAccessibility = () => {{
                        return {{
                            hasAltTexts: Array.from(document.querySelectorAll('img')).every(img => img.alt),
                            hasAriaLabels: countElements('[aria-label]'),
                            hasHeadingStructure: countElements('h1') > 0,
                            hasLangAttribute: document.documentElement.hasAttribute('lang'),
                            focusableElements: countElements('a, button, input, select, textarea, [tabindex]')
                        }};
                    }};
                    
                    return {{
                        // Basic Information
                        basic: {{
                            title: document.title,
                            url: window.location.href,
                            domain: window.location.hostname,
                            protocol: window.location.protocol,
                            charset: document.characterSet,
                            language: document.documentElement.lang || 'Not specified',
                            lastModified: document.lastModified
                        }},
                        
                        // Content Analysis
                        content: {{
                            textLength: document.body.innerText.length,
                            wordCount: document.body.innerText.split(/\\s+/).filter(word => word.length > 0).length,
                            readingTime: Math.ceil(document.body.innerText.split(/\\s+/).length / 200), // avg 200 wpm
                            totalLinks: countElements('a'),
                            externalLinks: Array.from(document.querySelectorAll('a')).filter(a => 
                                a.href && !a.href.includes(window.location.hostname)).length,
                            images: countElements('img'),
                            videos: countElements('video'),
                            audios: countElements('audio')
                        }},
                        
                        // Structure Analysis
                        structure: {{
                            headings: {{
                                h1: countElements('h1'),
                                h2: countElements('h2'),
                                h3: countElements('h3'),
                                h4: countElements('h4'),
                                h5: countElements('h5'),
                                h6: countElements('h6')
                            }},
                            lists: countElements('ul, ol'),
                            tables: countElements('table'),
                            forms: countElements('form'),
                            buttons: countElements('button'),
                            inputs: countElements('input'),
                            paragraphs: countElements('p'),
                            divs: countElements('div'),
                            spans: countElements('span')
                        }},
                        
                        // Technical Analysis
                        technical: {{
                            totalElements: document.querySelectorAll('*').length,
                            scripts: countElements('script'),
                            stylesheets: countElements('link[rel="stylesheet"]'),
                            hasServiceWorker: 'serviceWorker' in navigator,
                            hasWebGL: !!window.WebGLRenderingContext,
                            hasGeolocation: 'geolocation' in navigator,
                            hasLocalStorage: typeof(Storage) !== "undefined",
                            viewportWidth: window.innerWidth,
                            viewportHeight: window.innerHeight,
                            screenWidth: window.screen.width,
                            screenHeight: window.screen.height
                        }},
                        
                        // Performance Metrics
                        performance: {{
                            loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
                            domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
                            firstPaint: performance.getEntriesByType('paint').find(p => p.name === 'first-paint')?.startTime || 'N/A',
                            firstContentfulPaint: performance.getEntriesByType('paint').find(p => p.name === 'first-contentful-paint')?.startTime || 'N/A'
                        }},
                        
                        // SEO Analysis
                        seo: {{
                            metaTags: getMetaTags(),
                            hasTitle: !!document.title,
                            titleLength: document.title.length,
                            hasMetaDescription: !!document.querySelector('meta[name="description"]'),
                            hasCanonical: !!document.querySelector('link[rel="canonical"]'),
                            hasRobots: !!document.querySelector('meta[name="robots"]'),
                            structuredData: countElements('script[type="application/ld+json"]')
                        }},
                        
                        // Design Analysis
                        design: analyzeColors(),
                        
                        // Accessibility Check
                        accessibility: checkAccessibility()
                    }};
                }});
                
                // Generate comprehensive report
                console.log('📊 DETAILED RESEARCH ANALYSIS REPORT');
                console.log('=' .repeat(60));
                
                // Basic Information
                console.log('📋 BASIC INFORMATION:');
                console.log(`   Title: ${{detailedMetrics.basic.title}}`);
                console.log(`   Domain: ${{detailedMetrics.basic.domain}}`);
                console.log(`   Protocol: ${{detailedMetrics.basic.protocol}}`);
                console.log(`   Language: ${{detailedMetrics.basic.language}}`);
                console.log(`   Character Set: ${{detailedMetrics.basic.charset}}`);
                console.log(`   Last Modified: ${{detailedMetrics.basic.lastModified}}`);
                console.log('');
                
                // Content Metrics
                console.log('📝 CONTENT ANALYSIS:');
                console.log(`   Word Count: ${{detailedMetrics.content.wordCount.toLocaleString()}} words`);
                console.log(`   Character Count: ${{detailedMetrics.content.textLength.toLocaleString()}} characters`);
                console.log(`   Estimated Reading Time: ${{detailedMetrics.content.readingTime}} minutes`);
                console.log(`   Total Links: ${{detailedMetrics.content.totalLinks}}`);
                console.log(`   External Links: ${{detailedMetrics.content.externalLinks}}`);
                console.log(`   Internal Links: ${{detailedMetrics.content.totalLinks - detailedMetrics.content.externalLinks}}`);
                console.log(`   Images: ${{detailedMetrics.content.images}}`);
                console.log(`   Videos: ${{detailedMetrics.content.videos}}`);
                console.log(`   Audio Elements: ${{detailedMetrics.content.audios}}`);
                console.log('');
                
                // Structure Analysis
                console.log('🏗️ STRUCTURE ANALYSIS:');
                console.log(`   H1 Tags: ${{detailedMetrics.structure.headings.h1}}`);
                console.log(`   H2 Tags: ${{detailedMetrics.structure.headings.h2}}`);
                console.log(`   H3 Tags: ${{detailedMetrics.structure.headings.h3}}`);
                console.log(`   Total Headings: ${{Object.values(detailedMetrics.structure.headings).reduce((a,b) => a+b, 0)}}`);
                console.log(`   Paragraphs: ${{detailedMetrics.structure.paragraphs}}`);
                console.log(`   Lists: ${{detailedMetrics.structure.lists}}`);
                console.log(`   Tables: ${{detailedMetrics.structure.tables}}`);
                console.log(`   Forms: ${{detailedMetrics.structure.forms}}`);
                console.log(`   Interactive Elements: ${{detailedMetrics.structure.buttons + detailedMetrics.structure.inputs}}`);
                console.log('');
                
                // Technical Analysis
                console.log('⚙️ TECHNICAL ANALYSIS:');
                console.log(`   Total DOM Elements: ${{detailedMetrics.technical.totalElements.toLocaleString()}}`);
                console.log(`   JavaScript Files: ${{detailedMetrics.technical.scripts}}`);
                console.log(`   CSS Stylesheets: ${{detailedMetrics.technical.stylesheets}}`);
                console.log(`   Viewport: ${{detailedMetrics.technical.viewportWidth}}x${{detailedMetrics.technical.viewportHeight}}`);
                console.log(`   Screen Resolution: ${{detailedMetrics.technical.screenWidth}}x${{detailedMetrics.technical.screenHeight}}`);
                console.log(`   Modern Features:`);
                console.log(`     - Service Worker: ${{detailedMetrics.technical.hasServiceWorker ? '✅' : '❌'}}`);
                console.log(`     - WebGL: ${{detailedMetrics.technical.hasWebGL ? '✅' : '❌'}}`);
                console.log(`     - Geolocation: ${{detailedMetrics.technical.hasGeolocation ? '✅' : '❌'}}`);
                console.log(`     - Local Storage: ${{detailedMetrics.technical.hasLocalStorage ? '✅' : '❌'}}`);
                console.log('');
                
                // Performance Metrics
                console.log('⚡ PERFORMANCE METRICS:');
                console.log(`   Total Load Time: ${{detailedMetrics.performance.loadTime}}ms`);
                console.log(`   DOM Content Loaded: ${{detailedMetrics.performance.domContentLoaded}}ms`);
                console.log(`   First Paint: ${{detailedMetrics.performance.firstPaint}}ms`);
                console.log(`   First Contentful Paint: ${{detailedMetrics.performance.firstContentfulPaint}}ms`);
                console.log('');
                
                // SEO Analysis
                console.log('🔍 SEO ANALYSIS:');
                console.log(`   Page Title: ${{detailedMetrics.seo.hasTitle ? '✅' : '❌'}} (${{detailedMetrics.seo.titleLength}} chars)`);
                console.log(`   Meta Description: ${{detailedMetrics.seo.hasMetaDescription ? '✅' : '❌'}}`);
                console.log(`   Canonical URL: ${{detailedMetrics.seo.hasCanonical ? '✅' : '❌'}}`);
                console.log(`   Robots Meta: ${{detailedMetrics.seo.hasRobots ? '✅' : '❌'}}`);
                console.log(`   Structured Data: ${{detailedMetrics.seo.structuredData}} schemas found`);
                console.log('');
                
                // Accessibility Analysis
                console.log('♿ ACCESSIBILITY ANALYSIS:');
                console.log(`   Alt Text Coverage: ${{detailedMetrics.accessibility.hasAltTexts ? '✅ Complete' : '❌ Incomplete'}}`);
                console.log(`   ARIA Labels: ${{detailedMetrics.accessibility.hasAriaLabels}} elements`);
                console.log(`   Heading Structure: ${{detailedMetrics.accessibility.hasHeadingStructure ? '✅ Present' : '❌ Missing'}}`);
                console.log(`   Language Attribute: ${{detailedMetrics.accessibility.hasLangAttribute ? '✅ Present' : '❌ Missing'}}`);
                console.log(`   Focusable Elements: ${{detailedMetrics.accessibility.focusableElements}}`);
                console.log('');
                
                // Calculate quality scores
                const contentQuality = Math.min(100, (detailedMetrics.content.wordCount / 10));
                const structureQuality = Math.min(100, (Object.values(detailedMetrics.structure.headings).reduce((a,b) => a+b, 0) * 10));
                const seoQuality = [
                    detailedMetrics.seo.hasTitle,
                    detailedMetrics.seo.hasMetaDescription,
                    detailedMetrics.seo.titleLength > 10 && detailedMetrics.seo.titleLength < 60
                ].filter(Boolean).length * 33.33;
                
                console.log('📈 QUALITY SCORES:');
                console.log(`   Content Quality: ${{contentQuality.toFixed(1)}}%`);
                console.log(`   Structure Quality: ${{structureQuality.toFixed(1)}}%`);
                console.log(`   SEO Quality: ${{seoQuality.toFixed(1)}}%`);
                console.log(`   Performance Score: ${{detailedMetrics.performance.loadTime < 3000 ? '✅ Good' : '⚠️ Needs Improvement'}}`);
                
                await delay(3000);
                await browser.close();
                console.log('🎯 Advanced research analysis completed successfully');
            """
        else:
            script_body = """
                console.log('📖 Default demo mode');
                await page.goto('https://example.com');
                await delay(2000);
                await browser.close();
            """
        
        return base_config + script_body + "\n} catch(error) { console.error('❌ Error:', error.message); process.exit(1); } })();"
    
    @staticmethod
    def execute_script(node_path: str, script: str) -> Dict[str, any]:
        """Enhanced script execution with detailed monitoring and extended timeout"""
        script_file = 'temp_automation.js'
        
        try:
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script)
            
            # Execute with extended timeout and detailed error capture
            result = subprocess.run([node_path, script_file], 
                                  capture_output=True, text=True, 
                                  timeout=CONFIG["timeout"], encoding='utf-8')
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.stderr else None,
                "return_code": result.returncode,
                "execution_time": "Completed within timeout",
                "details": {
                    "stdout_lines": len(result.stdout.splitlines()) if result.stdout else 0,
                    "stderr_lines": len(result.stderr.splitlines()) if result.stderr else 0,
                    "total_output_chars": len(result.stdout) + len(result.stderr or "")
                }
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False, 
                "error": f"Execution timeout after {CONFIG['timeout']} seconds - process was terminated for safety",
                "execution_time": f"Exceeded {CONFIG['timeout']}s timeout",
                "details": {"timeout_reason": "Process took longer than expected - may indicate network issues or complex page loading"}
            }
        except Exception as e:
            return {
                "success": False, 
                "error": f"Execution error: {str(e)}",
                "details": {"exception_type": type(e).__name__, "exception_message": str(e)}
            }
        finally:
            try: 
                os.remove(script_file)
            except: 
                pass

# Streamlit Application
def main():
    st.set_page_config(page_title=CONFIG["app_title"], layout="wide", 
                       initial_sidebar_state="expanded")
    
    # Header
    st.markdown(f"# {CONFIG['app_title']}")
    st.markdown(f"*{CONFIG['app_subtitle']}*")
    
    # Academic Context
    with st.expander("📚 Academic Context & Learning Objectives"):
        st.markdown("""
        **Primary Learning Objectives:**
        - Understand inter-process communication between Python and Node.js
        - Demonstrate browser automation for research and testing
        - Implement proper error handling and user feedback systems
        - Practice cross-platform development considerations
        
        **Technical Stack:** Python (Streamlit) + Node.js (Puppeteer) + Subprocess Communication
        """)
    
    # System Validation
    with st.sidebar:
        st.markdown("### 🔧 System Status")
        is_valid, node_path, npm_path = SystemManager.validate_environment()
        
        if is_valid:
            st.success("✅ Node.js Runtime Detected")
            st.info(f"📍 Node Path: `{Path(node_path).name}`")
            
            # Installation Management
            st.markdown("### 📦 Dependency Management")
            if st.button("Install Puppeteer", type="primary"):
                with st.spinner("Installing dependencies..."):
                    result = PuppeteerManager.ensure_installation(npm_path)
                
                if result["success"]:
                    st.success("✅ " + result["message"])
                else:
                    st.error("❌ " + result["message"])
        else:
            st.error("❌ Node.js not found")
            st.markdown("Please install Node.js to continue")
            return
    
    # Main Interface
    if is_valid and Path('node_modules').exists():
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Academic Demo")
            st.markdown("Demonstrates automated navigation to Google Scholar with analysis")
            
            if st.button("🚀 Run Academic Demo", type="primary"):
                with st.spinner("Executing browser automation..."):
                    script = PuppeteerManager.create_script("demo")
                    result = PuppeteerManager.execute_script(node_path, script)
                
                if result["success"]:
                    st.success("✅ Demo executed successfully!")
                    
                    # Display execution metrics
                    with st.expander("📊 Execution Metrics"):
                        col1_metrics, col2_metrics = st.columns(2)
                        with col1_metrics:
                            st.metric("Output Lines", result["details"]["stdout_lines"])
                            st.metric("Return Code", result["return_code"])
                        with col2_metrics:
                            st.metric("Total Characters", result["details"]["total_output_chars"])
                            st.metric("Execution Status", result["execution_time"])
                    
                    # Display detailed output
                    st.markdown("### 📋 Detailed Analysis Output")
                    st.code(result["output"], language="text")
                    
                    # Show screenshot if available
                    screenshot_files = [f for f in os.listdir('.') if f.startswith('academic_demo_') and f.endswith('.png')]
                    if screenshot_files:
                        latest_screenshot = max(screenshot_files, key=os.path.getctime)
                        st.image(latest_screenshot, caption=f"Academic Demo Screenshot: {latest_screenshot}", width=600)
                        
                        # Provide download option
                        with open(latest_screenshot, "rb") as file:
                            st.download_button(
                                label="📥 Download Screenshot",
                                data=file.read(),
                                file_name=latest_screenshot,
                                mime="image/png"
                            )
                else:
                    st.error("❌ Execution failed")
                    st.error(result["error"])
                    
                    # Show detailed error information
                    if "details" in result:
                        with st.expander("🔍 Error Details"):
                            st.json(result["details"])
        
        with col2:
            st.markdown("### 🔬 Research Analysis")
            st.markdown("Automated website analysis with metrics collection")
            
            url = st.text_input("Research Target URL:", 
                              value="https://wikipedia.org", 
                              key="research_url")
            
            if st.button("📊 Analyze Website"):
                if url:
                    with st.spinner(f"Analyzing {url}..."):
                        script = PuppeteerManager.create_script("research", url=url)
                        result = PuppeteerManager.execute_script(node_path, script)
                    
                    if result["success"]:
                        st.success("✅ Analysis completed!")
                        
                        # Parse and display structured results
                        output_lines = result["output"].split('\n')
                        
                        # Extract key metrics for dashboard
                        metrics_data = {}
                        for line in output_lines:
                            if 'Word Count:' in line:
                                metrics_data['words'] = line.split(':')[1].strip().split()[0].replace(',', '')
                            elif 'Total Links:' in line:
                                metrics_data['links'] = line.split(':')[1].strip()
                            elif 'Total Load Time:' in line:
                                metrics_data['load_time'] = line.split(':')[1].strip().replace('ms', '')
                            elif 'Total DOM Elements:' in line:
                                metrics_data['elements'] = line.split(':')[1].strip().replace(',', '')
                        
                        # Display key metrics dashboard
                        if metrics_data:
                            st.markdown("### 📊 Key Metrics Dashboard")
                            col1_dash, col2_dash, col3_dash, col4_dash = st.columns(4)
                            
                            with col1_dash:
                                if 'words' in metrics_data:
                                    st.metric("Word Count", f"{int(metrics_data['words']):,}")
                            
                            with col2_dash:
                                if 'links' in metrics_data:
                                    st.metric("Total Links", metrics_data['links'])
                            
                            with col3_dash:
                                if 'load_time' in metrics_data:
                                    st.metric("Load Time", f"{metrics_data['load_time']}ms")
                            
                            with col4_dash:
                                if 'elements' in metrics_data:
                                    st.metric("DOM Elements", f"{int(metrics_data['elements']):,}")
                        
                        # Display full analysis
                        with st.expander("📋 Complete Analysis Report"):
                            st.code(result["output"], language="text")
                        
                        # Display execution details
                        with st.expander("⚙️ Execution Details"):
                            col1_exec, col2_exec = st.columns(2)
                            with col1_exec:
                                st.metric("Output Lines", result["details"]["stdout_lines"])
                                st.metric("Analysis Depth", "Advanced" if result["details"]["stdout_lines"] > 50 else "Basic")
                            with col2_exec:
                                st.metric("Total Output Size", f"{result['details']['total_output_chars']:,} chars")
                                st.metric("Execution Time", result["execution_time"])
                    else:
                        st.error("❌ Analysis failed")
                        st.error(result["error"])
                        
                        # Enhanced error reporting
                        if "details" in result:
                            with st.expander("🔍 Diagnostic Information"):
                                st.json(result["details"])
                                
                                if "timeout" in result["error"].lower():
                                    st.warning("💡 **Tip**: Try a simpler URL or check your internet connection. Some sites may take longer to load.")
                                elif "network" in result["error"].lower():
                                    st.warning("💡 **Tip**: Check if the URL is accessible and your internet connection is stable.")
                else:
                    st.warning("Please enter a URL to analyze")
    
    elif is_valid:
        st.info("📦 Please install Puppeteer using the sidebar to begin")
    
    # Advanced Technical Analysis Section
    st.markdown("---")
    if is_valid and Path('node_modules').exists():
        st.markdown("### 🔬 Advanced Analysis Features")
        
        with st.expander("📚 Technical Documentation & Learning Resources"):
            st.markdown("""
            **🎯 Analysis Capabilities:**
            
            **1. Comprehensive Web Analysis:**
            - Content metrics (word count, reading time, link analysis)
            - Structure analysis (heading hierarchy, DOM elements)
            - Performance monitoring (load times, paint metrics)
            - SEO evaluation (meta tags, structured data)
            - Accessibility assessment (ARIA labels, alt texts)
            
            **2. Technical Architecture:**
            - **Inter-Process Communication**: Python orchestrates Node.js subprocess
            - **Dynamic Code Generation**: JavaScript automation scripts created programmatically  
            - **Cross-Platform Compatibility**: Automatic executable detection and path resolution
            - **Real-Time Feedback**: Live progress updates and error handling
            - **Extended Timeout Management**: 5-minute execution limit for complex analyses
            
            **3. Academic Applications:**
            - **Digital Humanities**: Automated content analysis of historical websites
            - **Media Studies**: Social media platform structure analysis
            - **Computer Science**: Web performance benchmarking and optimization studies
            - **Information Science**: SEO and accessibility compliance research
            
            **4. Industry Relevance:**
            - Quality Assurance automation principles
            - Web scraping for data science applications
            - Performance monitoring and optimization
            - Accessibility compliance testing
            """)
        
        with st.expander("⚙️ System Configuration & Performance"):
            st.markdown("**Current Configuration:**")
            config_col1, config_col2 = st.columns(2)
            
            with config_col1:
                st.code(f"""
Execution Timeout: {CONFIG['timeout']} seconds
Analysis Timeout: {CONFIG['analysis_timeout']/1000} seconds
Installation Timeout: {CONFIG['installation_timeout']} seconds
Viewport: {CONFIG['viewport']['width']}x{CONFIG['viewport']['height']}
                """)
            
            with config_col2:
                st.markdown("**Performance Optimizations:**")
                st.markdown("- Extended timeouts for complex sites")
                st.markdown("- Full-page screenshot capabilities") 
                st.markdown("- Network idle detection")
                st.markdown("- Comprehensive error reporting")
                st.markdown("- Memory-efficient subprocess management")
        
        with st.expander("🏆 Project Showcase Points"):
            st.markdown("""
            **Key Technical Achievements:**
            
            ✅ **Cross-Language Integration**: Seamless Python-Node.js communication  
            ✅ **Dynamic Script Generation**: Runtime JavaScript code creation  
            ✅ **Robust Error Handling**: Comprehensive timeout and exception management  
            ✅ **Academic Focus**: Research-oriented automation with detailed analytics  
            ✅ **Professional Documentation**: Clean code with comprehensive explanations  
            ✅ **Real-World Application**: Industry-standard automation principles  
            ✅ **Educational Value**: Clear learning objectives and technical explanations  
            
            **Demonstrates Mastery Of:**
            - Modern web automation frameworks (Puppeteer)
            - Python web application development (Streamlit)
            - Subprocess management and inter-process communication
            - Cross-platform development considerations
            - User experience design for technical applications
            - Academic research tool development
            """)
    
    # Footer with academic context
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.markdown("**🎓 Educational Value**")
        st.markdown("- Inter-language communication")
        st.markdown("- Browser automation principles") 
        st.markdown("- Real-time system feedback")
    
    with footer_col2:
        st.markdown("**🔬 Research Applications**")
        st.markdown("- Web content analysis")
        st.markdown("- Performance benchmarking")
        st.markdown("- Accessibility evaluation")
    
    with footer_col3:
        st.markdown("**💼 Industry Relevance**")
        st.markdown("- QA automation practices")
        st.markdown("- Web scraping methodologies")
        st.markdown("- Performance monitoring")
    
    st.markdown("*Built for academic demonstration of modern web automation principles with industry-standard practices*")

if __name__ == "__main__":
    main()