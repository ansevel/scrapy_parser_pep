import datetime as dt
from collections import defaultdict

from pep_parse.settings import BASE_DIR, DATE_FROMAT


class PepParsePipeline:

    def open_spider(self, spider):
        self.pep_statuses = defaultdict(int)

    def process_item(self, item, spider):
        self.pep_statuses[item['status']] += 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_formatted = now.strftime(DATE_FROMAT)
        filename = f'status_summary_{now_formatted}.csv'
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        file_path = results_dir / filename
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status, count in self.pep_statuses.items():
                f.write(f'{status},{count}\n')
            f.write(f'Total,{sum(self.pep_statuses.values())}\n')
