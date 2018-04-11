#-*- coding: utf-8 -*-

# 总量指标
# 总借出(实际)金额
# 总借出人次
# 未还金额(包含逾期和未到期的应还金额，不包含逾期等费用)
# 未还逾期金额（应还金额，不包含逾期等费用）
SUMINDEX = """
	SELECT tt.firmId
		, tt.productId
		, IF(tt.loanSumMoney IS NOT NULL, tt.loanSumMoney, 0) AS loanSumMoney
		, IF(tt.loanSumPeopleNum IS NOT NULL, tt.loanSumPeopleNum, 0) AS loanSumPeopleNum
		, IF(tt.unpaidSumMoney IS NOT NULL, tt.unpaidSumMoney, 0) AS unpaidSumMoney
		, IF(tt.delaySumMoney IS NOT NULL, tt.delaySumMoney, 0) AS delaySumMoney
		, CURDATE() AS createDate
	FROM (
		SELECT t1.firmId
			, t1.productId
			, loanSumMoney
			, loanSumPeopleNum
			, unpaidSumMoney
			, delaySumMoney
		FROM (
			SELECT firmId
				, productId
				, SUM(payMoney) AS loanSumMoney
				, COUNT(DISTINCT userSid) AS loanSumPeopleNum
			FROM loan
			WHERE status = 6
				AND productId in ('{}')
				AND firmId in ('{}')
			GROUP BY firmId, productId
		) t1
		LEFT JOIN (
			SELECT firmId
				, productId
				, SUM(repayMoney) AS unpaidSumMoney
			FROM loan_repaying
			WHERE compatibleStatus != 'CANCEL'
				AND repaidTime IS NULL
				AND productId in ('{}')
				AND firmId in ('{}')
			GROUP BY firmId, productId
		) t2
		ON t1.firmId = t2.firmId
			AND t1.productId = t2.productId
		LEFT JOIN (
			SELECT firmId
				, productId
				, SUM(repayMoney) AS delaySumMoney
			FROM loan_repaying
			WHERE repaidTime IS NULL
				AND compatibleStatus != 'CANCEL'
				AND termDate < CURDATE()
				AND productId in ('{}')
				AND firmId in ('{}')
			GROUP BY firmId, productId
		) t3
		ON t1.firmId = t3.firmId
			AND t1.productId = t3.productId
	) tt
"""

#均量指标
# 平均每笔贷款金额(名义金额lendMoney)
# 平均每笔贷款周期
# 平均还款率(根据已到期订单的名义金额lendMoney计算)
AVGINDEX = """
	SELECT l1.firmId
		, l1.productId
		, IF(l1.avgLoanMoney IS NOT NULL, l1.avgLoanMoney, 0) AS avgLoanMoney
		, IF(l1.avgLoanTerm IS NOT NULL, l1.avgLoanTerm, 0) AS avgLoanTerm
		, IF(l2.paidMoney IS NOT NULL, l2.paidMoney / l1.loanSumMoney * 100, 0) AS avgRepayRate
		, CURDATE() AS createDate
	FROM (
		SELECT lr.firmId, lr.productId, AVG(l.lendMoney) AS avgLoanMoney, AVG(l.termNum) AS avgLoanTerm
			, SUM(CASE WHEN lr.termDate < CURDATE() THEN l.lendMoney ELSE 0 END) AS loanSumMoney
		FROM loan_repaying lr
		LEFT JOIN loan l
		ON lr.loanId = l.id
		WHERE l.status = 6
			AND lr.compatibleStatus != 'CANCEL'
			AND lr.productId in ('{}')
			AND lr.firmId in ('{}')
		GROUP BY lr.firmId, lr.productId
	) l1
	LEFT JOIN (
		SELECT lr.firmId, lr.productId, SUM(l.lendMoney) AS paidMoney
		FROM loan_repaying lr
		LEFT JOIN loan l
		ON lr.loanId = l.id
		WHERE lr.productId in ('{}')
			AND lr.compatibleStatus != 'CANCEL'
			AND l.status = 6
			AND lr.termDate < CURDATE()
			AND lr.repaidTime is not null
			AND lr.firmId in ('{}')
		GROUP BY lr.firmId, lr.productId
	) l2
	ON l1.firmId = l2.firmId
		AND l1.productId = l2.productId
"""
#每周借还款情况
# 每周贷出金额(名义金额lendMoney)(回款周对应的贷款金额，并非放款周对应的贷款金额)
# 每周还款金额(名义金额lendMoney, 并非repaidMoney)(回款周对应的还款金额)
# 每周逾期金额(名义)
# 每周逾期率

REPAIDMONEY = """
	SELECT l1.firmId
		, l1.productId
		, concat(year(l1.weekdate), '/', week(l1.weekdate)) AS 'week'
		, l1.weekdate
		, IF(allLoanMoney IS NOT NULL, allLoanMoney, 0) AS allLoanMoney
		, IF(paidMoney IS NOT NULL, paidMoney, 0) AS paidSumMoney
		, IF(paidMoney IS NOT NULL, allLoanMoney - paidMoney, 0) AS delaySumMoney
		, IF(paidMoney IS NOT NULL, round(paidMoney / allLoanMoney * 100, 2), 0) AS paidRate
		, CURDATE() AS createDate
	FROM (
		SELECT lr.firmId
			, lr.productId
			, date_sub(lr.termDate,INTERVAL WEEKDAY(lr.termDate) + 1 DAY) AS weekdate
			, SUM(l.lendMoney) AS allLoanMoney
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
			, SUM(l.lendMoney) AS paidMoney
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

#当期逾期天数分布
# 以回款周为时间周的逾期数据
OVERDUEDAY = """
	SELECT firmId
		, productId
		, SUM(CASE WHEN overdueday BETWEEN 0 AND 3 THEN 1 ELSE 0 END) AS overdueDayOnetoThree
		, SUM(CASE WHEN overdueday BETWEEN 4 AND 10 THEN 1 ELSE 0 END) AS overdueDayFourtoTen
		, SUM(CASE WHEN overdueday BETWEEN 11 AND 20 THEN 1 ELSE 0 END) AS overdueDayTentoTwoty
		, SUM(CASE WHEN overdueday BETWEEN 21 AND 30 THEN 1 ELSE 0 END) AS overdueDayTwotytoThreety
		, SUM(CASE WHEN overdueday BETWEEN 31 AND 60 THEN 1 ELSE 0 END) AS overdueDayThreetytoSixty
		, SUM(CASE WHEN overdueday BETWEEN 61 AND 90 THEN 1 ELSE 0 END) AS overdueDaySixtytoNinety
		, SUM(CASE WHEN overdueday > 90 THEN 1 ELSE 0 END) AS overdueDayOverNity
		, CURDATE() AS createDate
	FROM (
		SELECT lr.firmId
			, lr.productId
			, lr.termDate
			, lr.repaidTime
			, IF(lr.repaidTime IS NULL, DATEDIFF(CURDATE(),lr.termDate), DATEDIFF(lr.repaidTime, lr.termDate)) AS overdueday
		FROM loan_repaying lr
		LEFT OUTER JOIN loan l
		ON lr.loanId = l.id
		WHERE lr.compatibleStatus NOT IN ('CANCEL')
			AND l.status = 6
			AND lr.termDate < CURDATE()
			AND lr.productId in ('{}')
			AND lr.firmId in ('{}')
	) ll
	GROUP BY firmId, productId
"""

#周逾期率
# 以回款周为时间周的逾期数据(名义金额lendMoney)
OVERDUERATE = """
	SELECT firmId
		, productId
		, concat(year(weekdate), '/', week(weekdate)) AS 'week'
		, weekdate
		, loanMoney
		, round(100 - paidMoneyZero / loanMoney * 100, 2) AS overdueRateTzero
		, round(100 - paidMoneyThree / loanMoney * 100, 2) AS overdueRateTthree
		, round(100 - paidMoneySeven / loanMoney * 100, 2) AS overdueRateTseven
		, round(100 - paidMoneyFourteen / loanMoney * 100, 2) AS overdueRateTfourteen
		, round(100 - paidMoneyTwentyone / loanMoney * 100, 2) AS overdueRateTtwentyone
		, round(100 - paidMoneyThreety / loanMoney * 100, 2) AS overdueRateMone
		, round(100 - paidMoneySixty / loanMoney * 100, 2) AS overdueRateMtwo
		, round(100 - paidMoneyNinety / loanMoney * 100, 2) AS overdueRateMthree
		, CURDATE() AS createDate
	FROM (
	SELECT l1.firmId
		,l1.productId
		,l1.weekdate
		, SUM(l1.lendMoney) AS loanMoney
		, SUM(CASE WHEN l1.overdueday <= 0 THEN l1.lendMoney ELSE 0 END) AS paidMoneyZero
		, SUM(CASE WHEN l1.overdueday <= 3 THEN l1.lendMoney ELSE 0 END) AS paidMoneyThree
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