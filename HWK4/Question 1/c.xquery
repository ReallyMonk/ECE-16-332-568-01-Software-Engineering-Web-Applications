<products>
    {
        for $product in doc("a/xml")/products/product
        where $product/stores/store/markup = 25%
        return
        <product>
            {$product/name}
            {$product/price}
        </product>

    }
</products>