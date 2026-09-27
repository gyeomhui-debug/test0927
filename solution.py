"""의료급여 지원업무·기관 현황 일괄 집계 (Python 표준 라이브러리)."""
import argparse
import csv
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

BASE = Path(__file__).resolve().parent
WORK_NAME = '의료급여_대상자_지원업무_업무데이터.csv'
ORG_NAME = '의료급여_대상자_지원업무_기관현황.csv'


def read_csv(path, required):
    if not path.is_file():
        raise ValueError(f'필수 파일 없음: {path}')
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f'헤더 없음: {path}')
        missing = required - set(reader.fieldnames)
        if missing:
            raise ValueError(f'필수 헤더 누락 ({path.name}): {", ".join(sorted(missing))}')
        return list(reader)


def number(value, filename, row, field):
    try:
        result = Decimal(value.strip())
        if not result.is_finite():
            raise InvalidOperation
        return result
    except (AttributeError, InvalidOperation):
        raise ValueError(f'숫자 오류 ({filename}, 데이터 {row}행, {field}): {value!r}') from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, default=BASE / 'upload' / WORK_NAME)
    parser.add_argument('--org', type=Path, default=BASE / 'upload' / ORG_NAME)
    parser.add_argument('--output', type=Path, default=BASE / '결과_요약.csv')
    args = parser.parse_args()
    work = read_csv(args.work, {'업무ID', '업무유형', '처리상태', '처리기간_일'})
    org = read_csv(args.org, {'기관유형', '업무이수율'})
    periods = [number(r['처리기간_일'], args.work.name, i, '처리기간_일') for i, r in enumerate(work, 2)]
    rates = defaultdict(list)
    for i, r in enumerate(org, 2):
        rates[r['기관유형']].append(number(r['업무이수율'], args.org.name, i, '업무이수율'))
    rounded = lambda x, digits: str(x.quantize(Decimal(digits), rounding=ROUND_HALF_UP))
    result = [
        ('전체 업무 수', '', str(len(work))),
        ('완료 건수', '', str(sum(r['처리상태'] == '완료' for r in work))),
        ('평균 처리기간(일)', '', rounded(sum(periods) / len(periods), '1') if periods else '0'),
    ]
    result += [('업무유형별 건수', key, str(value)) for key, value in sorted(Counter(r['업무유형'] for r in work).items())]
    result += [('기관유형별 평균 업무이수율', key, rounded(sum(values) / len(values), '0.1')) for key, values in sorted(rates.items())]
    with args.output.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['지표', '구분', '값'])
        writer.writerows(result)
    for indicator, category, value in result:
        print(f'{indicator}{" / " + category if category else ""}: {value}')
    print(f'[OK] {args.output}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, ZeroDivisionError) as exc:
        print(f'[오류] {exc}', file=sys.stderr)
        sys.exit(1)
