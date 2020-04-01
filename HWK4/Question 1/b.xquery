<products>
    {
        for $product in doc("b.xml")/db/products/row
        return
            <product pid="{$product/pid}">
                {$product/name}
                {$product/price}
                {$profuct/description}
                <stores>
                {
                    for $store in doc("b.xml")/db/stores/row
                    for $markup in doc("b.xml")/db/sells/row
                    where $product/pid = $markup/pid and $store/sid = $markup/sid
                    return
                        <store sid="{$store/sid}">
                            {$store/name}
                            {$store/phones}
                            {$markup/markup}
                        </store>
                }
                </stores>
            </product>
    }
</prodcuts>