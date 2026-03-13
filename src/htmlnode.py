class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or self.props == {}:
            return ""
        prel_result = ""
        for key, value in self.props.items():

            prel_result = prel_result + key + '="' + value + '" '
        result = prel_result.rstrip()
        return result

    def __repr__(self):
        return (
                "This HTMLNode object has the following data members: "
                f"tag: {self.tag} "
                f"value: {self.value} "
                f"children: {self.children} "
                f"props: {self.props}"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        elif not self.tag:
            return str(self.value)
        elif self.tag == "img":
            props_html = self.props_to_html()
            return f'<{self.tag} {props_html} />'
        else:
            if self.props:
                props_html = self.props_to_html()
                return f'<{self.tag} {props_html}>{self.value}</{self.tag}>'
            else:
                return f'<{self.tag}>{self.value}</{self.tag}>'

    def __repr__(self):
        return (
                "This LeafNode object has the following data members: "
                f"tag: {self.tag} "
                f"value: {self.value} "
                f"props: {self.props} "
        )


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required")
        if not self.children:
            raise ValueError("Children are required")
        else:
            inner = ''
            for child in self.children:
                inner += child.to_html()
            result = f'<{self.tag}>{inner}</{self.tag}>'
            return result
