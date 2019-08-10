
(function (jQuery) {
    $.opt = {};  // jQuery Object

    jQuery.fn.invoice = function (options) {
        var ops = jQuery.extend({}, jQuery.fn.invoice.defaults, options);
        $.opt = ops;

        var inv = new Invoice();
        inv.init();

        jQuery('body').on('click', function (e) {
            var cur = e.target.id || e.target.className;

            if (cur == $.opt.addRow.substring(1))
                inv.newRow();

            if (cur == $.opt.delete.substring(1))
                inv.deleteRow(e.target);

            inv.init();
        });

        jQuery('body').on('keyup', function (e) {
            inv.init();
        });

        return this;
    };
}(jQuery));

function Invoice() {
    self = this;
}

Invoice.prototype = {
    constructor: Invoice,

    init: function () {
        this.calcTotal();
        this.calcTotalQty();
        this.calcSubtotal();
        this.calcGrandTotal();
//        this.calcPaidAmount();
        this.calcRemainingAmount();
        this.calcReturnedAmount();
    },

    /**
     * Calculate total price of an item.
     *
     * @returns {number}
     */
    calcTotal: function () {
         jQuery($.opt.parentClass).each(function (i) {
             var row = jQuery(this);
             var item_sub_price = row.find($.opt.price).val() * row.find($.opt.qty).val();

             // Uncomment when you want to use
             // var percent_discount = (item_sub_price * row.find($.opt.perdiscount).val())/100;
             //var total = item_sub_price - percent_discount;

             var total = row.find($.opt.price).val() * row.find($.opt.qty).val();
             total = self.roundNumber(total, 2);
             row.find($.opt.total).html(total);
         });

         return 1;
     },
	
    /***
     * Calculate total quantity of an order.
     *
     * @returns {number}
     */
    calcTotalQty: function () {
         var totalQty = 0;
         jQuery($.opt.qty).each(function (i) {
             var qty = jQuery(this).val();
             if (!isNaN(qty)) totalQty += Number(qty);
         });

         totalQty = self.roundNumber(totalQty, 2);

         jQuery($.opt.totalQty).html(totalQty);

         return 1;
     },

    /***
     * Calculate subtotal of an order.
     *
     * @returns {number}
     */
    calcSubtotal: function () {
         var subtotal = 0;
         jQuery($.opt.total).each(function (i) {
             var total = jQuery(this).html();
             if (!isNaN(total)) subtotal += Number(total);
         });

         subtotal = self.roundNumber(subtotal, 2);

         jQuery($.opt.subtotal).html(subtotal);

         return 1;
     },

    /**
     * Calculate grand total of an order.
     *
     * @returns {number}
     */
    calcGrandTotal: function () {
        var grandTotal = Number(jQuery($.opt.subtotal).html())
                       + Number(jQuery($.opt.shipping).val())
                       - Number(jQuery($.opt.discount).val());
        grandTotal = self.roundNumber(grandTotal, 2);

        jQuery($.opt.grandTotal).html(grandTotal);
        return 1;
    },

//    calcPaidAmount: function () {
//        var grandTotal = Number(jQuery($.opt.subtotal).html())
//                       + Number(jQuery($.opt.shipping).val())
//                       - Number(jQuery($.opt.discount).val());
//        grandTotal = self.roundNumber(grandTotal, 2);
//        jQuery($.opt.paidAmount).val(grandTotal);
//        return 1;
//    },

    calcRemainingAmount: function () {
        var remainingAmount = Number(jQuery($.opt.grandTotal).html())
                       - Number(jQuery($.opt.paidAmount).val());
        jQuery($.opt.remainingAmount).html(remainingAmount);
        return 1;
    },

    calcReturnedAmount: function () {
        var returnedAmount = Number(jQuery($.opt.cashPayment).val())
            - Number(jQuery($.opt.grandTotal).html());
        jQuery($.opt.returnedCash).html(returnedAmount);
        return 1;
    },

    /**
     * Add a row.
     *
     * @returns {number}
     */
    newRow: function () {
        // Uncomment after re using that
        // var percent_discount = '<td><select class="form-control perdiscount" id="sel1"><option>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option><option>7</option><option>8</option><option>9</option><option>10</option></select></td>';

        var item_list = '<datalist id="all-items">';
        $.get('/sales/product/items/details/', function (data, status) {
            $.each(data.products, function(key, result){
                item_list += '<option data-value="' + result.id + '" data-price="' + result.consumer_price + '" data-stock= "' + result.stock +'" value="' + result.name + '">' + result.name + '</option>'
            });
            item_list += '</datalist>';

            // Uncomment after re using that
            // jQuery(".item-row:last").after('<tr class="item-row"><td id="item-name" class="item-name"><div class="delete-btn"><input type="text" class="form-control invoice-item" id="invoice-item" name="all-items" list="all-items" placeholder="Select Item" type="text">'+ item_list +'<a class=' + $.opt.delete.substring(1) + ' href="javascript:;" title="Remove row">X</a></div></td><td><input class="form-control price" placeholder="Price" type="text"> </td><td><input class="form-control qty" placeholder="Quantity" value="1" type="text"></td>'+ percent_discount +'<td><span class="total">0.00</span></td></tr>');

            jQuery(".item-row:last").after('<tr class="item-row"><td id="item-name" class="item-name"><div class="delete-btn"><input type="text" class="form-control invoice-item" id="invoice-item" name="all-items" list="all-items" placeholder="Select Item" type="text">'+ item_list +'<a class=' + $.opt.delete.substring(1) + ' href="javascript:;" title="Remove row">X</a></div></td><td class="stock">0</td><td><input class="form-control price" placeholder="Price" type="text"> </td><td><input class="form-control qty" placeholder="Quantity" value="1" type="text"></td><td><span class="total">0.00</span></td></tr>');
            if (jQuery($.opt.delete).length > 0) {
                jQuery($.opt.delete).show();
            }
        });
        return 1;
    },

    /**
     * Delete a row.
     *
     * @param elem   current element
     * @returns {number}
     */
    deleteRow: function (elem) {
        jQuery(elem).parents($.opt.parentClass).remove();

        if (jQuery($.opt.delete).length < 2) {
            jQuery($.opt.delete).hide();
        }

        return 1;
    },

    /**
     * Round a number.
     * Using: http://www.mediacollege.com/internet/javascript/number/round.html
     *
     * @param number
     * @param decimals
     * @returns {*}
     */
    roundNumber: function (number, decimals) {
        var newString;// The new rounded number
        decimals = Number(decimals);

        if (decimals < 1) {
            newString = (Math.round(number)).toString();
        } else {
            var numString = number.toString();

            if (numString.lastIndexOf(".") == -1) {// If there is no decimal point
                numString += ".";// give it one at the end
            }

            var cutoff = numString.lastIndexOf(".") + decimals;// The point at which to truncate the number
            var d1 = Number(numString.substring(cutoff, cutoff + 1));// The value of the last decimal place that we'll end up with
            var d2 = Number(numString.substring(cutoff + 1, cutoff + 2));// The next decimal, after the last one we want

            if (d2 >= 5) {// Do we need to round up at all? If not, the string will just be truncated
                if (d1 == 9 && cutoff > 0) {// If the last digit is 9, find a new cutoff point
                    while (cutoff > 0 && (d1 == 9 || isNaN(d1))) {
                        if (d1 != ".") {
                            cutoff -= 1;
                            d1 = Number(numString.substring(cutoff, cutoff + 1));
                        } else {
                            cutoff -= 1;
                        }
                    }
                }

                d1 += 1;
            }

            if (d1 == 10) {
                numString = numString.substring(0, numString.lastIndexOf("."));
                var roundedNum = Number(numString) + 1;
                newString = roundedNum.toString() + '.';
            } else {
                newString = numString.substring(0, cutoff) + d1.toString();
            }
        }

        if (newString.lastIndexOf(".") == -1) {// Do this again, to the new string
            newString += ".";
        }

        var decs = (newString.substring(newString.lastIndexOf(".") + 1)).length;

        for (var i = 0; i < decimals - decs; i++)
            newString += "0";
        //var newNumber = Number(newString);// make it a number if you like

        return newString; // Output the result to the form field (change for your purposes)
    }
};

/**
 *  Publicly accessible defaults.
 */
jQuery.fn.invoice.defaults = {
    addRow: "#addRow",
    delete: ".delete",
    parentClass: ".item-row",

    price: ".price",
    qty: ".qty",
    total: ".total",
    totalQty: "#totalQty",
    // perdiscount: '.perdiscount',

    subtotal: "#subtotal",
    discount: "#discount",
    shipping: "#shipping",
    grandTotal: "#grandTotal",

    remainingAmount: '#remainingAmount',
    paidAmount: '#paidAmount',

    cashPayment: '#cash_payment',
    returnedCash: '#returned_cash',
};
