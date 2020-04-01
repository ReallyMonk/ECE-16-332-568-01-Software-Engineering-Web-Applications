<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/TR/WD-xsl"
                result-ns="http://www.w3.org/TR/REC-html">

<xsl:template match="/">
    <html>
        <head>
            <title>Bibliography</title>
        </head>
        <body background="antiquewhite">
            <center><h2>Bibliography</h2><hr width="90%"/></center>
            <ul>
                <xsl:for-each select="bib/book">
                    <p/><li>
                        <xsl:value-of select="author/last_name"/>,
                        <xsl:value-of select="author/first_name"/>.
                        <b><xsl:value-of select="title"/></b>
                        (<xsl:value-of select="publisher"/>
                        <xsl:value-of select="address">
                        <xsl:value-of select="year">).
                    </li>
                </xsl:for-each>

                <xsl:for-each select="bib/article">
                    </p><li>
                        <xsl:value-of select="author/last_name"/>,
                        <xsl:value-of select="author/first_name"/>.
                        <xsl:value-of select="title"/>,
                        <b><xsl:value-of select="journal"/>
                            <xsl:value-of select="volulme"/></b>
                        pp.<xsl:value-of select="page"/>
                        <xsl:value-of select="year">.
                    </li>
                </xsl:for-each>

                <xsl:for-each select="bib/phd_theses">
                    </p><li>
                        <xsl:value-of select="author/last_name"/>,
                        <xsl:value-of select="author/first_name"/>.
                        <b><xsl:value-of select="title"></b>
                        <xsl:value-of select="year">,
                        <xsl:value-of select="institution">,
                        <xsl:value-of slect="advisor">
                    </li>
                </xsl:for-each>
            </ul>
        </body>
    </html>
</xsl:template>

<xsl:template match="page">
    <xsl:value-of select="from"/>-<xsl:value-of select="to"/>,
</xsl:template>

</xsl:stylesheet>