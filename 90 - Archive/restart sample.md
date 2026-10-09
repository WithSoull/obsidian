``` bash
cp /usr/bin/telegraf /usr/bin/telegraf_old
rm /usr/bin/telegraf
cp ./telegraf /usr/bin/telegraf
pkill telegraf
```

``` bash
cp /usr/local/bin/mysync /usr/local/bin/mysync_old
rm /usr/local/bin/mysync
cp ./mysync /usr/local/bin/mysync
pkill mysync
```

``` bash
GOOS=linux go build -tags netgo,osusergo -o ./cmd/mysync/mysync ./cmd/mysync/... && pssh scp ./cmd/mysync/mysync klg-aksec4leqtqv32ec.mdb.yandex.net:/home/grishinid/ && pssh klg-aksec4leqtqv32ec.mdb.yandex.net
```

``` bash
GOOS=linux go build -tags netgo,osusergo -o ./cmd/mysync/mysync ./cmd/mysync/... && pssh scp ./cmd/mysync/mysync sas-clbfmnbue0hkk8nr.mdb.yandex.net:/home/grishinid/ && pssh sas-clbfmnbue0hkk8nr.mdb.yandex.net
```

``` bash
GOOS=linux go build -tags netgo,osusergo -o ./cmd/mysync/mysync ./cmd/mysync/... && pssh scp ./cmd/mysync/mysync vla-tsgeakh47tnt3ar4.mdb.yandex.net:/home/grishinid/ && pssh vla-tsgeakh47tnt3ar4.mdb.yandex.net
```

``` go
func (h *MySQLHealth) canWriteCheck(ctx context.Context) error {
	readOnly, err := isHostReadOnly(ctx, h.ConnectionName)
	if err != nil {
		return err
	}

	isMaster, err := isMaster(ctx, h.ConnectionName)
	if err != nil {
		return err
	}

	if isMaster && readOnly {
		return xerrors.Errorf("current master is readOnly")
	}
	bp, err := h.getBinlogPosition(ctx, h.ConnectionName)
	if err != nil {
		return err
	}
	if h.prevBinlogPos.Equal(bp) {
		return xerrors.Errorf("no one writes to the database")
	}
	h.prevBinlogPos = bp
	return nil
}
```