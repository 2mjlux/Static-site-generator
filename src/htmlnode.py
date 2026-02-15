class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        prel_result = ""
        for key, value in self.props.items():

            prel_result = prel_result + key + '="' + value + '" '
        result = prel_result.rstrip()
        return result

    def __repr__(self):
        print("This HTMLNode object has the following data members:")
        print(f"tag: {self.tag}")
        print(f"value: {self.value}")
        print(f"children: {self.children}")
        print(f"props: {self.props}")
