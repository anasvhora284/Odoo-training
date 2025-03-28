/**
 * Direct DOM script to help debug SBODR button visibility issues
 * This will run regardless of the module system
 */
(function() {
    console.log("SBODR DEBUG: Direct script loaded");
    
    function initDebug() {
        console.log("SBODR DEBUG: Initializing direct debug script");
        
        // Check for SBODR elements
        const sbodrButtons = document.querySelectorAll(".sbodr-request");
        const debugInfo = document.getElementById("sbodr_debug_info");
        
        console.log(`SBODR DEBUG: Found ${sbodrButtons.length} buttons`);
        
        // Make debug info always visible
        if (debugInfo) {
            debugInfo.style.display = "block";
            const status = debugInfo.querySelector("#sbodr_debug_status");
            if (status) {
                status.textContent = `Direct debug script found ${sbodrButtons.length} buttons`;
            }
        } else {
            console.log("SBODR DEBUG: No debug info element found");
        }
        
        // Try to extract product info
        try {
            const productId = getProductIdFromPage();
            console.log(`SBODR DEBUG: Product ID: ${productId || 'not found'}`);
            
            // Add click handlers if buttons exist
            if (sbodrButtons.length) {
                sbodrButtons.forEach(btn => {
                    console.log("SBODR DEBUG: Adding click handler to button");
                    btn.addEventListener("click", function(e) {
                        e.preventDefault();
                        console.log("SBODR DEBUG: Button clicked");
                        alert("SBODR button clicked! This is from the direct debug script.");
                    });
                });
            }
        } catch (error) {
            console.error("SBODR DEBUG: Error in debug script", error);
        }
    }
    
    function getProductIdFromPage() {
        // Try to find product ID from URL or DOM
        const urlParams = new URLSearchParams(window.location.search);
        const productId = urlParams.get("product_id");
        if (productId) return productId;
        
        const productInput = document.querySelector('input[name="product_id"]');
        if (productInput && productInput.value) return productInput.value;
        
        const addToCartForm = document.getElementById("add_to_cart");
        if (addToCartForm && addToCartForm.dataset.productId) {
            return addToCartForm.dataset.productId;
        }
        
        return null;
    }
    
    // Initialize when DOM is ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initDebug);
    } else {
        initDebug();
    }
})();
