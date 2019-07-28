class SiteQueue:

    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def is_empty(self):
        return self.items == []

    def add(self, site_name: str, site_ip: str, site_port: int):
        self.items.insert(0, (site_name, site_ip, site_port))

    def dequeue(self):
        return self.items.pop()

    def show(self):
        return self.items

    def is_in(self, site_name):
        if site_name in self.items:
            return True
        else:
            return False
