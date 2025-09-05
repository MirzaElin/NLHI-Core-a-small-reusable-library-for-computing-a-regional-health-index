import argparse, csv, json, sys
import pandas as pd
from . import core
from .io import Store

def _read_domains(path):
    if path.lower().endswith(('.xlsx','.xls')):
        book = pd.read_excel(path, sheet_name=None)
        df = book.get('Data', next(iter(book.values())))
    else:
        df = pd.read_csv(path)
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})
    if 'name' not in df.columns:
        for alt in ['domain','Domain','DOMAIN']:
            if alt in df.columns:
                df = df.rename(columns={alt:'name'})
    return df

def main(argv=None):
    p = argparse.ArgumentParser(prog='nlhi', description='NLHI Core CLI')
    sub = p.add_subparsers(dest='cmd', required=True)

    sp = sub.add_parser('compute')
    sp.add_argument('--age', type=float, required=True)
    sp.add_argument('--pop', type=float, required=True)
    sp.add_argument('--le', type=float, required=True)
    sp.add_argument('domains_path')

    sp = sub.add_parser('add-record')
    sp.add_argument('--region', required=True)
    sp.add_argument('--date', required=True)
    sp.add_argument('--age', type=float, required=True)
    sp.add_argument('--pop', type=float, required=True)
    sp.add_argument('--le', type=float, required=True)
    sp.add_argument('domains_path')
    sp.add_argument('store_path')

    sp = sub.add_parser('summarize')
    sp.add_argument('--region', required=True)
    sp.add_argument('store_path')

    sp = sub.add_parser('plot')
    sp.add_argument('--region', required=True)
    sp.add_argument('--out', default='nlhi_timeseries.png')
    sp.add_argument('store_path')

    args = p.parse_args(argv)

    if args.cmd == 'compute':
        df = _read_domains(args.domains_path)
        rec = core.compute_record(args.age, args.pop, args.le, df)
        print(json.dumps(rec, indent=2))
    elif args.cmd == 'add-record':
        df = _read_domains(args.domains_path)
        rec = core.compute_record(args.age, args.pop, args.le, df)
        store = Store(args.store_path)
        store.upsert(args.region, args.date, rec)
        print(json.dumps({'status':'ok','region':args.region,'date':args.date,'NLHI':rec['NLHI']}, indent=2))
    elif args.cmd == 'summarize':
        store = Store(args.store_path)
        out = store.time_series(args.region)
        print(json.dumps(out, indent=2))
    elif args.cmd == 'plot':
        try:
            import matplotlib.pyplot as plt
        except Exception as e:
            raise SystemExit("matplotlib required for plotting: pip install 'nlhi[plot]'")
        store = Store(args.store_path)
        ts = store.time_series(args.region)
        if not ts:
            raise SystemExit('No data for region.')
        dates = [t['date'] for t in ts]
        vals = [t['NLHI'] for t in ts]
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(dates, vals, marker='o')
        ax.set_title(f'NLHI over time — {args.region}')
        ax.set_ylabel('NLHI (avg DSAV %)')
        ax.grid(True)
        fig.autofmt_xdate()
        fig.tight_layout()
        fig.savefig(args.out, dpi=150)
        print(json.dumps({'status':'ok','out':args.out}, indent=2))
    else:
        p.print_help()

if __name__ == '__main__':
    main()
