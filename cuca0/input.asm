start:
	ldi 10
	write var1
	ldi 20
	add var1
	; acc = 30 here

end:
	halt

.var var1 0
.var var2 0
.var var3 0
