(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cdr (cdr s)))
)


(define (sign num)
  (cond
    ((> num 0) 1)
    ((= num 0) 0)
    (else -1))
)


(define (square x) (* x x))

(define (pow x y)
  (cond
    ((= y 0) 1)
    ((even? y) (square (pow x (/ y 2))))
    ((odd? y) (* x (square (pow x (/ (- y 1) 2))))))
)


(define (unique s)
  (if (null? s) '()
    (cons (car s) (unique (filter (lambda (x) (not (equal? x (car s))))
      (cdr s)))))

)


(define (replicate x n)
  (define (helper n acc)
    (if (= n 0)
      acc
      (helper (- n 1) (cons x acc))))
    (helper n nil)  

  )


(define (accumulate combiner start n term)
  (define (range n)
    (define (helper x)
      (if (> x n)
        nil
        (cons x (helper (+ 1 x)))))
    (helper 1))
    (define (reduce-default combiner lst default)
      (reduce combiner (cons default lst)))
    (reduce-default combiner (map term (range n)) start)
)


(define (accumulate-tail combiner start n term)
  (define (helper x acc)
    (if (> x n)
      acc
      (helper (+ 1 x) (combiner acc (term x)))))
  (helper 1 start)
)


(define-macro (list-of map-expr for var in lst if filter-expr)
  `(map (lambda (, var) ,map-expr) (filter (lambda (, var) ,filter-expr) ,lst))
)

