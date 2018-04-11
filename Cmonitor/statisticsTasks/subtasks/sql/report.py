#-*- coding: utf-8 -*-

#总还款报表 累积指标
# 总贷款金额(名义金额 lendMoney)
# 总贷款支付金额(实际支付金额 payMoney)
# 总还款金额(实际回款金额 repaidMoney)
# 总待收金额(应还金额 repayMoney 不包含逾期费用等)
ALLLOAN = """
	SELECT l1.firmId
		, l1.productId
		, concat(year(CURDATE()), '/', week(CURDATE())) AS 'week'
		, date_sub(CURDATE(),INTERVAL WEEKDAY(CURDATE()) + 1 DAY) AS 'weekDate'
		, IF(allLoanCount IS NOT NULL, allLoanCount, 0) AS allLoanCount
		, IF(allLoanMoney IS NOT NULL, allLoanMoney, 0) AS allLoanMoney
		, IF(allPayMoney IS NOT NULL, allPayMoney, 0) AS allPayMoney
		, IF(allPaidCount IS NOT NULL, allPaidCount, 0) AS allPaidCount
		, IF(allPaidMoney IS NOT NULL, allPaidMoney, 0) AS allPaidMoney
		, IF(allNoPaidCount IS NOT NULL, allNoPaidCount, 0) AS allNoPaidCount
		, IF(allNoPaidMoney IS NOT NULL, allNoPaidMoney, 0) AS allNoPaidMoney
		, CURDATE() AS createDate
	FROM (
		SELECT lr.firmId
			, lr.productId
			, COUNT(1) AS allLoanCount
			, SUM(l.lendMoney) AS allLoanMoney
			, SUM(l.payMoney) AS allPayMoney
		FROM loan_repaying lr, loan l
		WHERE lr.loanId = l.id
			AND lr.compatibleStatus NOT IN ('CANCEL')
			AND l.status = 6
			AND lr.termDate < CURDATE()
			AND lr.productId in ('{}')
			AND lr.firmId in ('{}')
		GROUP BY lr.firmId, lr.productId
	) l1
	LEFT OUTER JOIN (
		SELECT lr.firmId
			, lr.productId
			, SUM(lr.repayMoney) AS allPaidMoney
			, COUNT(1) AS allPaidCount
		FROM loan_repaying lr, loan l
		WHERE lr.loanId = l.id
			AND lr.compatibleStatus NOT IN ('CANCEL')
			AND l.status = 6
			AND lr.termDate < CURDATE()
			AND lr.productId in ('{}')
			AND lr.firmId in ('{}')
			AND lr.repaidTime IS NOT NULL
			AND lr.repaidTime <= date_sub(lr.termDate,INTERVAL WEEKDAY(lr.termDate) - 5 DAY)
		GROUP BY lr.firmId, lr.productId
	) l2
	ON l1.firmId = l2.firmId AND l1.productId = l2.productId
	LEFT OUTER JOIN (
		SELECT lr.firmId
			, lr.productId
			, SUM(lr.repayMoney) AS allNoPaidMoney
			, COUNT(1) AS allNoPaidCount
		FROM loan_repaying lr, loan l
		WHERE lr.loanId = l.id
			AND lr.compatibleStatus NOT IN ('CANCEL')
			AND l.status = 6
			AND lr.termDate < CURDATE()
			AND lr.productId in ('{}')
			AND lr.firmId in ('{}')
			AND lr.repaidTime IS NULL
		GROUP BY lr.firmId, lr.productId
	) l3
	ON l1.firmId = l3.firmId  AND l1.productId = l3.productId
"""


#周借还款报表
# 每周贷出金额(名义金额lendMoney)(回款周对应的贷款金额，并非放款周对应的贷款金额)
# 每周贷出支付金额(实际金额payMoney)(回款周对应的贷款金额，并非放款周对应的贷款金额)
# 每周还款金额(实际金额repaidMoney)(回款周对应的还款金额)
# 每周逾期金额(名义)

WEEKLOAN = """
	SELECT l1.firmId
		, l1.productId
		, concat(year(l1.weekdate), '/', week(l1.weekdate)) AS 'week'
		, l1.weekdate
		, IF(weekLoanCount IS NOT NULL, weekLoanCount, 0) AS weekLoanCount
		, IF(weekLoanMoney IS NOT NULL, weekLoanMoney, 0) AS weekLoanMoney
		, IF(weekPayMoney IS NOT NULL, weekPayMoney, 0) AS weekPayMoney
		, IF(weekPaidCount IS NOT NULL, weekPaidCount, 0) AS weekPaidCount
		, IF(weekPaidMoney IS NOT NULL, weekPaidMoney, 0) AS weekPaidMoney
		, CURDATE() AS createDate
	FROM (
		SELECT lr.firmId
			, lr.productId
			, date_sub(lr.termDate,INTERVAL WEEKDAY(lr.termDate) + 1 DAY) AS weekdate
			, COUNT(1) AS weekLoanCount
			, SUM(l.lendMoney) AS weekLoanMoney
			, SUM(l.payMoney) AS weekPayMoney
		FROM loan_repaying lr, loan l
		WHERE lr.loanId = l.id
			AND lr.compatibleStatus NOT IN ('CANCEL')
			AND l.status = 6
			AND lr.termDate < CURDATE()
			AND lr.productId in ('{}')
			AND lr.firmId in ('{}')
		GROUP BY lr.firmId, lr.productId, 
			weekdate
	) l1
	LEFT OUTER JOIN (
		SELECT lr.firmId
			, lr.productId
			, date_sub(lr.termDate,INTERVAL WEEKDAY(lr.termDate) + 1 DAY) AS weekdate
			, SUM(lr.repaidMoney) AS weekPaidMoney
			, COUNT(1) AS weekPaidCount
		FROM loan_repaying lr, loan l
		WHERE lr.loanId = l.id
			AND lr.compatibleStatus NOT IN ('CANCEL')
			AND l.status = 6
			AND lr.termDate < CURDATE()
			AND lr.productId in ('{}')
			AND lr.firmId in ('{}')
			AND lr.repaidTime IS NOT NULL
			AND lr.repaidTime <= date_sub(lr.termDate,INTERVAL WEEKDAY(lr.termDate) - 5 DAY)
		GROUP BY lr.firmId, lr.productId,
			weekdate
	) l2
	ON l1.firmId = l2.firmId
		AND l1.productId = l2.productId
		AND l1.weekdate = l2.weekdate
"""

#周逾期报表
# 以回款周为时间周的逾期数据(名义金额lendMoney)
WEEKOVERDUE = """
	SELECT firmId
		, productId
		, concat(year(weekdate), '/', week(weekdate)) AS 'week'
		, weekdate
		, termMoney
		, termMoney - paidMoneySeven AS overdueMoneyTseven
		, termMoney - paidMoneyFourteen AS overdueMoneyTfourteen
		, termMoney - paidMoneyTwentyone AS overdueMoneyTtwentyone
		, termMoney - paidMoneyThreety AS overdueMoneyMone
		, termMoney - paidMoneySixty AS overdueMoneyMtwo
		, termMoney - paidMoneyNinety AS overdueMoneyMthree
		, round(100 - paidMoneySeven / termMoney * 100, 2) AS overdueRateTseven
		, round(100 - paidMoneyFourteen / termMoney * 100, 2) AS overdueRateTfourteen
		, round(100 - paidMoneyTwentyone / termMoney * 100, 2) AS overdueRateTtwentyone
		, round(100 - paidMoneyThreety / termMoney * 100, 2) AS overdueRateMone
		, round(100 - paidMoneySixty / termMoney * 100, 2) AS overdueRateMtwo
		, round(100 - paidMoneyNinety / termMoney * 100, 2) AS overdueRateMthree
		, CURDATE() AS createDate
	FROM (
	SELECT l1.firmId
		, l1.productId
		, l1.weekdate
		, SUM(l1.lendMoney) AS termMoney
		, SUM(CASE WHEN l1.overdueday <= 7 THEN l1.lendMoney ELSE 0 END) AS paidMoneySeven
		, SUM(CASE WHEN l1.overdueday <= 14 THEN l1.lendMoney ELSE 0 END) AS paidMoneyFourteen
		, SUM(CASE WHEN l1.overdueday <= 21 THEN l1.lendMoney ELSE 0 END) AS paidMoneyTwentyone
		, SUM(CASE WHEN l1.overdueday <= 30 THEN l1.lendMoney ELSE 0 END) AS paidMoneyThreety
		, SUM(CASE WHEN l1.overdueday <= 60 THEN l1.lendMoney ELSE 0 END) AS paidMoneySixty
		, SUM(CASE WHEN l1.overdueday <= 90 THEN l1.lendMoney ELSE 0 END) AS paidMoneyNinety
	FROM (
	SELECT lr.firmId
		, lr.productId
		, date_sub(lr.termDate,INTERVAL WEEKDAY(lr.termDate) + 1 DAY) AS weekdate
		, l.lendMoney
		, lr.termDate
		, lr.repaidTime
		, IF(lr.repaidTime IS NULL, DATEDIFF(CURDATE(),lr.termDate), DATEDIFF(lr.repaidTime,lr.termDate)) AS overdueday
	FROM loan_repaying lr, loan l
		WHERE lr.loanId = l.id
			AND lr.compatibleStatus NOT IN ('CANCEL')
			AND l.status = 6
			AND lr.termDate < CURDATE()
			AND lr.productId in ('{}')
			AND lr.firmId in ('{}')
	) l1
	GROUP BY
	l1.firmId, l1.productId, l1.weekdate
	) s1
"""